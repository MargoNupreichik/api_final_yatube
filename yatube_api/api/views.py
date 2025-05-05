from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        list_of_actions = ['update', 'partial_update', 'destroy', 'retrieve']
        if self.action in list_of_actions:
            return [IsOwnerOrReadOnly()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class GroupViewSet(RetrieveListViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(
            post=post,
            author=self.request.user
        )

    def get_permissions(self):
        list_of_actions = ['update', 'partial_update', 'destroy']
        if self.action in list_of_actions:
            return [IsOwnerOrReadOnly()]
        else:
            return [IsAuthenticated()]
