from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
    user=request.user
).order_by("-created_at")

    notifications.update(
        is_read=True
    )

    return render(
        request,
        "notifications/list.html",
        {
            "notifications": notifications
        }
    )

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def delete_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.delete()

    return redirect("notifications")