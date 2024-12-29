from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password1  = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2  = serializers.CharField(write_only=True, required=True)
    type       = serializers.CharField(required=False)

    class Meta:
        model  = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "type",
            "password1",
            "password2",
        )

    def validate(self, attrs):
        try:
            if self.context['request'].method in ['PATCH', 'PUT']:
                attrs.pop('password1', None)
                attrs.pop('password2', None)
        except:
            if attrs['password1'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2","")
        password1 = validated_data.pop("password1","")
        user_obj = User(**validated_data)
        user_obj.set_password(password1)
        user_obj.save()
        return user_obj
    
class UserLoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserBasicDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "type",
        )