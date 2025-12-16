from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from django.contrib import messages


def homepage(request):
    return render(request, "core/home.html")


def register_view(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def search_rooms(request):
    query = request.GET.get("q", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    floor = request.GET.get("floor", "")

    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(room_number__icontains=query)

    if min_price:
        rooms = rooms.filter(room_type__base_price__gte=min_price)

    if max_price:
        rooms = rooms.filter(room_type__base_price__lte=max_price)

    if floor:
        rooms = rooms.filter(floor=floor)

    return render(request, "core/search.html", {
        "rooms": rooms,
        "query": query,
        "min_price": min_price,
        "max_price": max_price,
        "floor": floor,
    })


def room_list(request):
    rooms = Room.objects.all()

    room_number = request.GET.get("room_number")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    floor = request.GET.get("floor")

    if room_number:
        rooms = rooms.filter(room_number__icontains=room_number)

    if min_price:
        rooms = rooms.filter(room_type__base_price__gte=min_price)

    if max_price:
        rooms = rooms.filter(room_type__base_price__lte=max_price)

    if floor:
        rooms = rooms.filter(floor=floor)

    if not request.GET:
        rooms = rooms[:4]

    return render(request, "core/room_list.html", {
        "rooms": rooms
    })

def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    photos = room.photos.all()

    return render(request, "core/room_detail.html", {
        "room": room,
        "photos": photos,
    })

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        Booking.objects.create(
            guest=request.user,
            room=room,
            checkin_date=request.POST.get("checkin_date"),
            checkout_date=request.POST.get("checkout_date"),
            status="pending",
        )
        # Вместо одной строки messages.success(...) вставь это:

    if request.LANGUAGE_CODE == 'kk':
        messages.success(request, "Бөлме сәтті брондалды! 'Менің брондарым' бөлімін тексеріңіз.")
    else:
        messages.success(request, "Room booked successfully! Check My Bookings.")
        return redirect("room_detail", id=room.id)

    return render(request, "core/book_room.html", {"room": room})


@login_required
def mybookings(request):
    bookings = Booking.objects.filter(
        guest=request.user,
        status="pending"
    )
    return render(request, "core/mybookings.html", {
        "bookings": bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    booking.status = "cancelled"
    booking.save()
    # Внутри cancel_booking:

    if request.LANGUAGE_CODE == 'kk':
        messages.warning(request, "Брондаудан бас тартылды.")
    else:
        messages.warning(request, "Booking has been cancelled.")
    return redirect("mybookings")
