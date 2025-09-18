from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Position, Department, Employee



class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'email': {'required': False}

        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.full_name', read_only=True, allow_null=True)

    class Meta:
        model = Department
        fields = ['id', 'code', 'name', 'manager', 'manager_name', 'is_active']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserCreationSerializer(write_only=True)

    user_name = serializers.CharField(source='user.username', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'user_name',
            'emp_code',
            'full_name',
            'email',
            'phone',
            'position',
            'position_name',
            'department',
            'department_name',
            'is_active'
        ]
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserCreationSerializer().create(validated_data=user_data)

        employee = Employee.objects.create(user=user, **validated_data)

        return employee

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.user.id
        return representation