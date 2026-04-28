from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message

def dashboard(request):
    if request.user.is_authenticated:
        inbox_count = Message.objects.filter(receiver=request.user, is_draft=False).count()
        sent_count = Message.objects.filter(sender=request.user, is_draft=False).count()
        draft_count = Message.objects.filter(sender=request.user, is_draft=True).count()
    else:
        inbox_count = sent_count = draft_count = 0

    return render(request, 'messages_app/dashboard.html', {
        'inbox_count': inbox_count,
        'sent_count': sent_count,
        'draft_count': draft_count,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'messages_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'messages_app/register.html')

@login_required
def inbox(request):
    query = request.GET.get('q', '')
    msgs = Message.objects.filter(receiver=request.user, is_draft=False)

    if query:
        msgs = msgs.filter(subject__icontains=query)

    return render(request, 'messages_app/inbox.html', {
        'messages_list': msgs,
        'query': query,
        'page_title': 'Inbox',
    })

@login_required
def sent(request):
    query = request.GET.get('q', '')
    msgs = Message.objects.filter(sender=request.user, is_draft=False)

    if query:
        msgs = msgs.filter(subject__icontains=query)

    return render(request, 'messages_app/sent.html', {
        'messages_list': msgs,
        'query': query,
        'page_title': 'Sent Messages',
    })

@login_required
def drafts(request):
    msgs = Message.objects.filter(sender=request.user, is_draft=True)
    return render(request, 'messages_app/drafts.html', {
        'messages_list': msgs,
        'page_title': 'Drafts',
    })

@login_required
def new_message(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        is_draft = 'save_draft' in request.POST

        if not receiver_id or not subject or not content:
            messages.error(request, 'Please complete all fields.')
            return render(request, 'messages_app/new_message.html', {'users': users})

        receiver = get_object_or_404(User, id=receiver_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            content=content,
            is_draft=is_draft
        )

        if is_draft:
            messages.success(request, 'Message saved as draft.')
            return redirect('drafts')

        messages.success(request, 'Message sent successfully.')
        return redirect('sent')

    return render(request, 'messages_app/new_message.html', {'users': users})

@login_required
def view_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)

    if msg.receiver != request.user and msg.sender != request.user:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('inbox')

    if msg.receiver == request.user:
        msg.is_read = True
        msg.save()

    return render(request, 'messages_app/view_message.html', {'message_obj': msg})

@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)

    if msg.receiver == request.user or msg.sender == request.user:
        msg.delete()
        messages.success(request, 'Message deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this message.')

    return redirect('inbox')
