from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        model = Post

    def create(self, validated_data):
        if 'group' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        group = validated_data.pop('group')
        post = Post.objects.create(**validated_data, group=group)
        return post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User .objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def create(self, validated_data):
        following = validated_data.pop('following')
        user = self.context['request'].user
        follow = Follow.objects.create(user=user,
                                       following=following)
        return follow

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if user == following:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя.")
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора.")
        return data
