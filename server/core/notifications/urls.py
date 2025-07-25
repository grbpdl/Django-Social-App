from django.urls import path

from .views import PushNotificationView, NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('push/', PushNotificationView.as_view(), name='push-notification'),
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
]
