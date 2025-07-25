# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # All auth routes now under /api/auth/
     # Post APIs
    path('api/posts/', include('posts.urls')),
     # Comment  APIs
    path('api/comments/', include('comments.urls')),
     # Poslikes  APIs
    path('api/likes/', include('likes.urls')),
     # Ratings  APIs
    path('api/ratings/', include('ratings.urls')),

    # Messaging & Premium Chat
    path('api/chat/', include('chat.urls')),

    # Notifications
    path('api/notifications/', include('notifications.urls')),

    # (Optional) Category filter/search
    # path('api/categories/', include('categories.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)