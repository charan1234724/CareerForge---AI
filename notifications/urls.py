from django.urls import path
from .views import notification_list, delete_notification

urlpatterns = [

    path(
        "notifications/",
        notification_list,
        name="notifications"
    ),
    path(
    "delete/<int:notification_id>/",
    delete_notification,
    name="delete_notification",
),

]