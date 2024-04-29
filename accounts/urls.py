from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("account/", views.account, name="account"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("", views.home, name="home"),
    path("sell/", views.sell, name="sell"),
    path("shop/", views.shop, name="shop"),
    path("seller-items/", views.seller_items, name="seller_items"),
    path("send-message/<int:item_id>/", views.send_message, name="send_message"),
    path("buyer-messages/", views.buyer_messages, name="buyer_messages"),
    path("seller-messages/", views.seller_messages, name="seller_messages"),
    path(
        "handle-message/<int:message_id>/", views.handle_message, name="handle_message"
    ),
    path(
        "send-additional-message/<int:message_id>/",
        views.send_additional_message,
        name="send_additional_message",
    ),
]
