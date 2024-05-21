from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Group, Post
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
        if self.kwargs.get('post_pk') is None:
            raise NotFound("Post not found.")
        return self.get_post().comments.all()

    def get_post(self):
        post_id = self.kwargs.get('post_pk')
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return None

    def perform_create(self, serializer):
        post = self.get_post()
        if post:
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
        )
