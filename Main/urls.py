from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("", views.home, name="home"),
    path("logout/", views.user_logout, name="logout"),
    path("account/", views.account, name="account"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("sell/", views.sell, name="sell"),
    path("shop/", views.shop, name="shop"),
    path("product_detail/<int:item_id>/", views.product_detail, name="product_detail"),
    path("received-orders/", views.received_orders, name="received_orders"),
    path("accept-order/<int:order_id>/", views.accept_order, name="accept_order"),
    path("decline-order/<int:order_id>/", views.decline_order, name="decline_order"),
    path("order_success/<int:order_id>/", views.order_success, name="order_success"),
    path("your_orders/", views.your_orders, name="your_orders"),
    path("your_items/", views.your_items, name="your_items"),
    path("update_item/<int:item_id>/", views.update_item, name="update_item"),
    path("user_info/<str:username>/", views.user_info, name="user_info"),
]
