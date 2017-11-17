from rest_framework import serializers
from .models import Value2, TimeStamp, Device, Register


# Memo, PeopleToWhom, PeopleWho, MemoStatus  # Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('id', 'x')


class ValueSerializer(serializers.ModelSerializer):
    # register = serializers.CharField(read_only=True, source="register.title")
    # device = serializers.CharField(read_only=True, source="register.device.title")
    date = serializers.DateTimeField(read_only=True, source="date.date")

    class Meta:
        model = Value2
        fields = ('id', 'date', 'value')


class Value2Serializer(serializers.ModelSerializer):
    time_stamp = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='x',
    )

    class Meta:
        model = Value2
        fields = ('id', 'time_stamp', 'value')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('id', 'title', 'last_value', 'last_time')


class DeviceSerializer(serializers.ModelSerializer):
    registers = RegisterSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('title', 'registers')


class ValueInRegSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, source="date.date")
    reg_title = serializers.StringRelatedField(read_only=True, source="register.title")
    reg_id = serializers.IntegerField(read_only=True, source="register.id")

    class Meta:
        model = Value2
        lookup_fields = 'reg_id'
        fields = ('reg_id', 'reg_title', 'id', 'date', 'value')

    # values = ValueSerializer(many=True, read_only=True)
    #
    # # device = serializers.CharField(read_only=True, source="device.title")
    #
    # class Meta:
    #     model = Register
    #     fields = ('id', 'title', 'values')


class ValueInDevSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, source="date.date")
    reg_title = serializers.StringRelatedField(read_only=True, source="register.title")
    reg_id = serializers.IntegerField(read_only=True, source="register.id")
    dev_title = serializers.StringRelatedField(read_only=True, source="register.device.title")
    dev_id = serializers.IntegerField(read_only=True, source="register.device.id")

    class Meta:
        model = Value2
        fields = ('dev_id', 'dev_title', 'reg_id', 'reg_title', 'id', 'date', 'value')
