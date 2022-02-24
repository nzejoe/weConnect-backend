from rest_framework import serializers

from .models import Account, UserFollower


class UserFollowSerializer(serializers.ModelSerializer):
    # this will serialize following user 
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'gender', 'avatar', 'followers']


class FollowersSerializer(serializers.ModelSerializer):
    follower = UserFollowSerializer()
    class Meta:
        model = UserFollower
        fields = '__all__'
        
        
class FollowingSerializer(serializers.ModelSerializer):
    following = UserFollowSerializer()
    class Meta:
        model = UserFollower
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    followers = FollowersSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField(method_name='get_full_name')
    class Meta:
        model = Account
        exclude = ['password', ]
        extra_kwargs = {
            'is_active': {
                'read_only': True,
            },
            'is_staff': {
                'read_only': True,
            },
            'is_admin': {
                'read_only': True,
            },
            'is_superuser': {
                'read_only': True,
            },
        }
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        return super().update(instance, validated_data)
    
    def get_full_name(self, data):
        return data.full_name


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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        
        if not Account.object.filter(email=value.lower()).exists():
            raise serializers.ValidationError(f'{value} is not associated with any account!')
        
        return value


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    password2 = serializers.CharField(max_length=30)
    
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'the two password did not match!'})
        return super().validate(attrs)
    
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    password2 = serializers.CharField(max_length=30)
    
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        
        # check if current password is correct
        if password != password2:
            raise serializers.ValidationError({'error': 'the new password did not match!'})
        return super().validate(attrs)

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'avatar']
