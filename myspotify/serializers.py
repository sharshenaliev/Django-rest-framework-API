from rest_framework import serializers
from .models import Music, CustomUser


class MusicListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = Music
        fields = ('id', 'name', 'author', 'album', 'genre', 'year_published', 'image', 'audio')
        read_only_fields = ('name', 'author', 'album', 'genre', 'year_published', 'image', 'audio')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'gender', 'age', 'password')

    def create(self, request):
        user = CustomUser.objects.create(username=request['username'], email=request['email'],
                                         first_name=request['first_name'],
                                         age=request['age'], gender=request['gender'])
        user.set_password(request['password'])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class EmailCheckSerializer(serializers.Serializer):
    gmail = serializers.CharField(required=True)

