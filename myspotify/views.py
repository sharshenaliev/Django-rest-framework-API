from rest_framework import generics, permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Favorites
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .service import MusicFilter
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.core.mail import send_mail
from django.db.models import F, Q


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    model = CustomUser
    permission_classes = (permissions.AllowAny,)

    def post(self, request, user_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get("new_password") == serializer.data.get("confirm_password"):
                if len(serializer.data.get("confirm_password")) >= 8:
                    user = CustomUser.objects.get(pk=user_id)
                    user.set_password(serializer.data.get("confirm_password"))
                    user.save()
                    return Response({'message': 'Password updated successfully'})
                else:
                    return Response({'message': 'Password is too short'})
            else:
                return Response({'message': "Passwords don't match"})
        return Response({'message': "Password can't be blank"})


class EmailCheckView(generics.GenericAPIView):
    serializer_class = EmailCheckSerializer
    model = CustomUser
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("gmail")
            try:
                user = CustomUser.objects.get(username=username)
                message = 'Hello, ' + user.first_name + \
                          ', here is your link to reset password: http://127.0.0.1:8000/api/user/' + str(user.id) + '/'
                send_mail(
                    'Subject - Django Email Testing',
                    message,
                    'sender@example.com',  # API mail sender
                    [
                        username,
                    ]
                )
                return Response({'message': "Mail sent"})
            except:
                return Response({'message': "User is not found"})
        return Response({'message': "Gmail can't be blank"})


class MusicListView(generics.ListAPIView):
    serializer_class = MusicListSerializer
    filter_backens = (DjangoFilterBackend,)
    filterset_class = MusicFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        music = Music.objects.all()
        return music

    def post(self, request):
        song = Music.objects.get(pk=request.data['id'])
        favorite, created = Favorites.objects.get_or_create(user=self.request.user, song=song)
        if created is False:
            message = "Song was deleted from Favorites"
            favorite.delete()
        else:
            message = "Song was added to Favorites"
            Music.objects.filter(id=song.id).update(popularity=F('popularity') + 1)
        path = request.get_full_path()
        path = path.split('/')
        link = list(filter(None, path))
        print(link)
        data = {
            'message': message,
            'url': reverse(link[-1], request=request)
        }
        return Response(data)


class MusicDetailView(generics.ListAPIView):
    def get(self, request, music_id):
        music = Music.objects.get(id=music_id)
        serializer = MusicDetailSerializer(music)
        return Response(serializer.data)


class MusicFavouriteListView(generics.ListAPIView):
    serializer_class = MusicListSerializer
    filter_backens = (DjangoFilterBackend,)
    filterset_class = MusicFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        favorite = Favorites.objects.filter(user=self.request.user).values_list('song')
        music = Music.objects.filter(id__in=favorite)
        return music

    def post(self, request):
        song = Music.objects.get(pk=request.data['id'])
        favorite = Favorites.objects.get(user=self.request.user, song=song)
        favorite.delete()
        data = {
            'message': "Song was deleted from Favorites",
            'url': reverse('favorites', request=request)
        }
        return Response(data)


class MusicPopularListView(MusicListView):
    def get_queryset(self):
        music = Music.objects.order_by('popularity')
        return music


class MusicNewListView(MusicListView):
    def get_queryset(self):
        music = Music.objects.filter(new=True).reverse()
        return music


class MusicRecomenmendListView(MusicListView):
    def get_queryset(self):
        favorite = Favorites.objects.filter(user=self.request.user).values_list('song')
        if favorite:
            authors = Music.objects.filter(id__in=favorite).values_list('author')
            genres = Music.objects.filter(id__in=favorite).values_list('genre')
            recommendation = Music.objects.filter(Q(author__in=authors) | Q(genre__in=genres))
        else:
            recommendation = Music.objects.order_by('popularity')
        return recommendation
