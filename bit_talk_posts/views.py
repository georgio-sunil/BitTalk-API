from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostsSerializer
from .models import Posts


class PostsViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)

    serializer_class = PostsSerializer

    def get_queryset(self):
        return Posts.objects.all()

    @action(detail=True, methods=['patch'],
            url_path=r'like/(?P<user_id>[^/.]+)')
    def add_like(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
                            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if kwargs['user_id'] not in instance.liked_by:
            instance.liked_by.append(kwargs['user_id'])
            instance.no_of_likes += 1
            instance.save()
        return Response(serializer.data)
