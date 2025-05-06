from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer, FollowSerializer
)
from rest_framework import viewsets, filters, mixins
from .permissions import IsOwnerOrReadOnly, ReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django import http


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        list_of_actions = ['update', 'partial_update', 'destroy', 'retrieve']
        if self.action in list_of_actions:
            return [IsOwnerOrReadOnly()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [ReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class GroupViewSet(RetrieveListViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        return http.HttpResponseNotAllowed(['GET', 'HEAD', 'OPTIONS'])

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [ReadOnly()]


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
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [ReadOnly()]


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]  # Добавляем поддержку поиска
    search_fields = ['following__username']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
