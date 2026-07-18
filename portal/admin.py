from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Property, PropertyImage, Booking

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'rent', 'bedrooms', 'bathrooms', 'available')
    list_filter = ('city', 'bedrooms', 'furnished', 'parking', 'available')
    search_fields = ('title', 'city', 'address')
    inlines = [PropertyImageInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'email', 'phone', 'move_in_date', 'status', 'created_at')
    list_filter = ('status', 'move_in_date', 'created_at')
    search_fields = ('property__title', 'user__email', 'email', 'phone')
    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        updated = queryset.update(status='Approved')
        # We manually save each to trigger post_save signals for sending status change emails
        for booking in queryset:
            booking.save()
        self.message_user(request, f"Successfully approved {queryset.count()} booking requests.")
    approve_bookings.short_description = "Approve selected booking requests"

    def reject_bookings(self, request, queryset):
        updated = queryset.update(status='Rejected')
        for booking in queryset:
            booking.save()
        self.message_user(request, f"Successfully rejected {queryset.count()} booking requests.")
    reject_bookings.short_description = "Reject selected booking requests"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'full_name', 'phone', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone', 'password'),
        }),
    )
