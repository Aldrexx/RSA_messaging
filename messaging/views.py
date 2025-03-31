from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Message, User
from .forms import RegisterForm, MessageForm

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    users = User.objects.all().order_by('username')
    messages_list = Message.objects.all().order_by('-timestamp')
    return render(request, 'admin.html', {
        'users': users,
        'messages': messages_list
    })

@login_required
@user_passes_test(is_admin)
def toggle_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
    return redirect('admin_panel')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.generate_keys()
            login(request, user)
            return redirect('inbox')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
    # Decrypt received messages
    decrypted_received = []
    for msg in received_messages:
        try:
            decrypted_text = msg.decrypt_message(request.user.private_key)
            decrypted_received.append({
                'id': msg.id,
                'sender': msg.sender,
                'text': decrypted_text,
                'timestamp': msg.timestamp
            })
        except Exception as e:
            messages.error(request, f"Could not decrypt message: {str(e)}")
    
    context = {
        'received_messages': decrypted_received,
        'sent_messages': sent_messages,
    }
    return render(request, 'inbox.html', {'context': context})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():

            recipient = form.cleaned_data['recipient']
            
            # Prevent sending messages to self
            if recipient == request.user:
                messages.error(request, "You cannot send a message to yourself.")
                return redirect('send_message')
            
            message = form.save(commit=False)
            message.sender = request.user
            recipient = message.recipient
            plaintext = form.cleaned_data['plaintext_message']
            message.encrypt_message(plaintext, recipient.public_key)
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if the user is a superuser (admin)
    if request.user.is_superuser:
        
        message.delete()
        messages.success(request, "Message deleted successfully!")
    # Check if the user is the sender or the recipient
    elif message.sender == request.user or message.recipient == request.user:
        message.delete()
        messages.success(request, "Message deleted successfully!")
    else:
        messages.error(request, "You don't have permission to delete this message!")
    
    return redirect('inbox')


