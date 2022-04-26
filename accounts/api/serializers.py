from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn`t match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

        # def create(self, validated_data):
        #     if validated_data.get('password') != validated_data.get('confirm_password'):
        #         raise serializers.ValidationError("Those password don't match")
        #
        #     elif validated_data.get('password') == validated_data.get('confirm_password'):
        #         validated_data['password'] = make_password(
        #             validated_data.get('password')
        #         )
        #
        #     return super(UserSerializer, self).create(validated_data)


# class UserPublicSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'url', 'username']
#
#     def get_url(self, obj):
#         request = self.context.get('request')
#         return reverse("user-detail", kwargs={'username': obj.username}, request=request)
