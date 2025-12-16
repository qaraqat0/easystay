from django.urls import path
from . import views
from django.conf.urls.i18n import set_language

urlpatterns = [
    path("", views.homepage, name="home"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("rooms/", views.room_list, name="room_list"),
    path("rooms/<int:id>/", views.room_detail, name="room_detail"),
    path("rooms/<int:room_id>/book/", views.book_room, name="book_room"),

    path("mybookings/", views.mybookings, name="mybookings"),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),

    path("set_language/", set_language, name="set_language"),
]