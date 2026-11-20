from .models import Notification




def create_notification( recipient, title,message, notification_type=Notification.NotificationType.GENERAL, link=''):
    return Notification.objects.create(
        recipient=recipient, title=title,
        message=message,notification_type=notification_type,link=link
    )




def notify_users(recipients, title, message, notification_type=Notification.NotificationType.GENERAL, link=''):
    notifications = [
        Notification(
            recipient=user,title=title, message=message,
            notification_type=notification_type, link=link
        )
        for user in recipients
    ]
    return Notification.objects.bulk_create(notifications)







