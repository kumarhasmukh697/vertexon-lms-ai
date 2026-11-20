from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer






class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)

        # Optional filtering:
        # ?is_read=false
        is_read = self.request.query_params.get('is_read')

        if is_read == 'true':
            queryset = queryset.filter(is_read=True)

        elif is_read == 'false':
            queryset = queryset.filter(is_read=False)

        return queryset





class UnreadNotificationCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter( recipient=request.user, is_read=False).count()
        return Response({'unread_count': unread_count})




class MarkNotificationReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):

        notification = get_object_or_404( Notification, id=notification_id, recipient=request.user )

        notification.is_read = True
        notification.save(update_fields=['is_read'])

        return Response( NotificationSerializer(notification).data, status=status.HTTP_200_OK)




class MarkAllNotificationsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        updated_count = Notification.objects.filter( recipient=request.user, is_read=False).update(is_read=True)

        return Response({
            'message': 'All notifications marked as read.',
            'updated_count': updated_count
        })
