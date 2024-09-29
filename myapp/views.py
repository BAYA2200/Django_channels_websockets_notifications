from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Отправляем уведомление через Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Новый пост создан: {response.data["title"]}'
            }
        )

        return response
