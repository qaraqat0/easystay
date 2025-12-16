from django.contrib import admin
from .models import RoomType, Room, RoomPhoto, Booking, Payment, Registration

# Для комнат показываем номер, цену и тип сразу в списке
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'floor')
    list_filter = ('room_type', 'floor')
    search_fields = ('room_number',)

# Для бронирований самое важное - видеть статус, даты и гостя
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'checkin_date', 'status')
    list_filter = ('status', 'checkin_date')
    search_fields = ('guest__username', 'room__room_number')
    list_editable = ('status',) # Позволяет менять статус прямо из общего списка!

# Остальные можно оставить простыми, если хочешь
admin.site.register(RoomType)
admin.site.register(RoomPhoto)
admin.site.register(Payment)
admin.site.register(Registration)