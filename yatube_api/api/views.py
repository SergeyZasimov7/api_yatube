from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post
from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, IsAuthorOrReadOnly)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)
