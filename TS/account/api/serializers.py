from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from account.models import User, ContactUs

class RegistrationSerializer(serializers.ModelSerializer):

    password  = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = (
			'username',
			'email',
			'phone',
			'state',
            'gender',
            'education',
            'first_name',
            'surname',
            'password',
            'password2',
            'dob'
			)

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError({"Username":"User already exists, please login"})
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError({"Email":"Email already exists, please login"})
        return value

    def validate_phone(self, value):
        qs = User.objects.filter(phone__iexact=value)
        if qs.exists():
            raise serializers.ValidationError({"phone":"Phone number already exists, please login"})
        return value

    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError({"Passsword":"Password must be more than 6 characters long"})
        if not any(letter.isdigit() for letter in value):
            raise serializers.ValidationError({"Passsword":"Password must contain a number"})

        return value

    def validate(self, data):
        """
        Validates the password length + authenticity and dob format
        """
        pw  = data.get('password')
        pw2 = data.get('password2')
        dob = data.get('dob')
        first_name = data.get('first_name')
        surname = data.get('surname')

        if not dob:
            raise serializers.ValidationError({'dob':'Give us a dob'})

        if not surname:
            raise serializers.ValidationError({'surname':'Your surname'})

        if not first_name:
            raise serializers.ValidationError({'first_name':'What is your first name?'})

        if pw != pw2:
            raise serializers.ValidationError({'password':'Password must match.'})
        try:
            dob =  dob.split('-')
            if len(dob[0]) != 4 or len(dob[1]) != 2 or len(dob[2]) != 2:
                raise serializers.ValidationError({'dob':'Pass numbers in the format YYYY-MM-DD please'})
        except:
            raise serializers.ValidationError({'dob':'Pass numbers in the format YYYY-MM-DD please'})

        return data


    def create(self, validated_data):
        normalized_email = User.objects.normalize_email(validated_data.get('email'))
        account = User(
            email =normalized_email,
            username = validated_data['username'].lower(),
            phone = validated_data['phone'],
            state = validated_data['state'],
            dob = validated_data['dob'],
            first_name = validated_data['first_name'],
            surname = validated_data['surname']
        )
        password = validated_data['password']

        account.set_password(password)
        account.save()
        return account



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'surname', 'state', 'phone', 'address', 'dob', 'total_questions',
        'total_upvotes', 'total_downvotes', 'total_answers', 'ts_rank']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'user', 'device_type', 'subject', 'message', 'spare']