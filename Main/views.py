from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from .models import UserProfile, Item, Order
from .forms import UserSignupForm, UpdateProfileForm, ChangePasswordForm, ItemForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserSignupForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def home(request):
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 6 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    elif 18 <= hour < 24:
        greeting = "Good evening"
    else:
        greeting = "Hello"
    return render(request, "home.html", {"greeting": greeting})


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def account(request):
    user = request.user
    name = user.userprofile.name
    email = user.userprofile.email
    phone_number = user.userprofile.phone_number
    return render(
        request,
        "account.html",
        {"user": user, "email": email, "name": name, "phone_number": phone_number},
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
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return render(request, "item_listed.html")
    else:
        form = ItemForm()
    return render(request, "sell.html", {"form": form})


@login_required
def shop(request):
    items = Item.objects.all()
    query = request.GET.get("q")
    if query:
        items = items.filter(description__icontains=query) and items.filter(
            name__icontains=query
        )
    availability = request.GET.get("availability")
    if availability == "available":
        items = items.filter(status="available")
    elif availability == "sold":
        items = items.filter(status="sold")
    return render(
        request,
        "shop.html",
        {"items": items, "query": query, "availability": availability},
    )


@login_required
def product_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        if item.status == "available":
            order = Order.objects.create(buyer=request.user, item=item)
            item.save()
            return HttpResponseRedirect(reverse("order_success", args=(order.id,)))
        else:
            return render(request, "item_not_available.html")
    else:
        return render(request, "product_detail.html", {"item": item})


@login_required
def order(request, item_id):
    item = Item.objects.get(pk=item_id)
    order = Order.objects.create(buyer=request.user, item=item)
    return HttpResponseRedirect(reverse("order_success", args=(order.id,)))


@login_required
def received_orders(request):
    received_orders = Order.objects.filter(item__seller=request.user)
    return render(request, "received_orders.html", {"orders": received_orders})


@login_required
def accept_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.item.seller == request.user:
        order.status = "accepted"
        order.comment = request.POST.get("comment", "")
        order.save()
        order.item.status = "sold"
        order.item.bought_by = order.buyer.username
        order.item.save()
        return render(request, "order_accepted.html", {"order": order})
    else:
        return render(request, "unauthorized_access.html")


@login_required
def decline_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.item.seller == request.user:
        order.status = "declined"
        order.comment = request.POST.get("comment", "")
        order.save()

        return render(request, "order_declined.html", {"order": order})
    else:
        return render(request, "unauthorized_access.html")


@login_required
def order_success(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, "order_success.html", {"order": order})


@login_required
def your_orders(request):
    user_orders = Order.objects.filter(buyer=request.user)
    return render(request, "your_orders.html", {"user_orders": user_orders})


@login_required
def your_items(request):
    seller_items = Item.objects.filter(seller=request.user)
    return render(request, "your_items.html", {"seller_items": seller_items})


@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("your_items")
    else:
        form = ItemForm(instance=item)
    return render(request, "update_item.html", {"form": form})


@login_required
def user_info(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    user_items = Item.objects.filter(seller=user_profile.user)
    return render(
        request,
        "user_info.html",
        {"user_profile": user_profile, "user_items": user_items},
    )
