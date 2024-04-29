from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Item, Message
from .forms import MinimalSignupForm
from .forms import UpdateProfileForm
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from .forms import ItemForm
from .forms import MessageForm
from django.http import HttpResponseBadRequest
from django.contrib import messages as django_messages


def signup(request):
    if request.method == "POST":
        form = MinimalSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = MinimalSignupForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


@login_required
def home(request):
    return render(request, "home.html")


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def account(request):
    user = request.user
    email = user.userprofile.email
    name = user.userprofile.name  # Add this line to fetch the name
    roll_number = user.userprofile.roll_number  # Add this line to fetch the roll number
    return render(
        request,
        "account.html",
        {"user": user, "email": email, "name": name, "roll_number": roll_number},
    )


@login_required
def update_profile(request):
    user = request.user
    profile = user.userprofile
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = UpdateProfileForm(instance=profile)
    return render(request, "update_profile.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("account")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, "change_password.html", {"form": form})


@login_required
def sell(request):
    return render(request, "sell.html")


@login_required
def shop(request):
    items = Item.objects.all()
    return render(request, "shop.html", {"items": items})


@login_required
def seller_items(request):
    seller_items = Item.objects.filter(user=request.user)
    return render(request, "seller_items.html", {"seller_items": seller_items})


@login_required
def sell(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect("seller_items")
    else:
        form = ItemForm()
    return render(request, "sell.html", {"form": form})


@login_required
def send_message(request, item_id):
    item = Item.objects.get(pk=item_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = item.user
            message.item = item
            message.save()
            messages.success(request, "Your message has been sent.")
            return redirect("shop")
    else:
        form = MessageForm()
    return render(request, "send_message.html", {"form": form, "item": item})


@login_required
def buyer_messages(request):
    messages = Message.objects.filter(sender=request.user)
    return render(request, "buyer_messages.html", {"messages": messages})


@login_required
def seller_messages(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, "seller_messages.html", {"messages": messages})


@login_required
def handle_message(request, message_id):
    if request.method == "POST":
        action = request.POST.get("action")
        message = Message.objects.get(pk=message_id)
        if action == "accept":
            message.status = "accepted"
            message.save()
            # Send message to buyer
            buyer_message = Message.objects.create(
                sender=request.user,
                receiver=message.sender,
                item=message.item,
                content="Your offer has been accepted. The seller has agreed to sell the item.",
                status="accepted",
            )
            # Update item status
            message.item.status = "sold"
            message.item.save()
            django_messages.success(request, "Message sent to buyer.")
        elif action == "decline":
            message.status = "declined"
            message.save()
            # Send message to buyer
            buyer_message = Message.objects.create(
                sender=request.user,
                receiver=message.sender,
                item=message.item,
                content="Your offer has been declined. The seller has decided not to sell the item.",
                status="declined",
            )
            django_messages.success(request, "Message sent to buyer.")
        return redirect("seller_messages")
    return HttpResponseBadRequest("Invalid request")


@login_required
def send_additional_message(request, message_id):
    if request.method == "POST":
        additional_message = request.POST.get("additional_message")
        if additional_message:
            message = Message.objects.get(pk=message_id)
            new_message = Message.objects.create(
                sender=request.user,
                receiver=message.sender,
                item=message.item,
                content=additional_message,
                status="pending",
            )
            django_messages.success(request, "Additional message sent to buyer.")
            return redirect("seller_messages")
        else:
            django_messages.error(request, "Please enter a message.")
    return HttpResponseBadRequest("Invalid request")
