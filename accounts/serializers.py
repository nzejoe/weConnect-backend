from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'gender', 'avatar']
        # exclude = ['password', ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'the two password did not match!'})
        
        return super().validate(attrs)