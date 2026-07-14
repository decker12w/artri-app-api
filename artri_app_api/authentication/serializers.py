# authentication/serializers.py
from rest_framework import serializers
from .models import Remedy, RemedyIntake, Exercise, Training, TrainingReport, DailyPainReport, User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RemedySerializer(serializers.ModelSerializer):
    class Meta:
        model = Remedy
        fields = '__all__'
        read_only_fields = ('user',)

class RemedyIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemedyIntake
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class TrainingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingReport
        fields = '__all__'
        read_only_fields = ('user',)

class DailyPainReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPainReport
        fields = '__all__'
        read_only_fields = ('user',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'weight', 'height'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date', None),
            weight=validated_data.get('weight', None),
            height=validated_data.get('height', None),
        )
        return user