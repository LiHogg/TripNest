# from django.db import models
# from django.contrib.auth.models import User
#
#
# # === BOOKING ===
# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
#     status = models.CharField(max_length=50, null=True, blank=True)
#     check_in = models.DateField(null=True, blank=True)
#     check_out = models.DateField(null=True, blank=True)
#     total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"Booking #{self.id} — {self.user.username}"
#
#
# # === BOOKING TYPE MAPPING ===
# class BookingTypeMapping(models.Model):
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='type_mappings')
#     draftbooking = models.ForeignKey('DraftBooking', on_delete=models.SET_NULL, null=True, blank=True)
#     item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='mappings')
#     recommendation_id = models.BigIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"Mapping {self.id} — Booking {self.booking.id}"
#
#
# # === DRAFTBOOKING ===
# class DraftBooking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='draft_bookings')
#     draft_detail = models.JSONField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"DraftBooking {self.id} — User {self.user.username}"
#
#
# # === ITEM ===
# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     reference_id = models.BigIntegerField(null=True, blank=True)
#     item_type = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.name} - {self.price} ₽"
