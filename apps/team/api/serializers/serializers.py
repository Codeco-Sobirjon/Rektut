from rest_framework import serializers

from apps.team.models import *


class TeamRoleListSerializers(serializers.ModelSerializer):
    """ Team Role create update and details """

    class Meta:
        model = TeamRole
        fields = ['id', 'name']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class TeamListSerializers(serializers.ModelSerializer):
    """ Team create update"""

    role = serializers.IntegerField(required=True)
    photo = serializers.ImageField(required=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'photo', 'role', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        role_id = validated_data.pop('role')
        role = TeamRole.objects.get(pk=role_id)  # Fetch the TeamRole instance
        team = Team.objects.create(**validated_data, role=role)
        return team

    def update(self, instance, validated_data):
        if 'role' in validated_data:
            role_id = validated_data.pop('role')
            instance.role = TeamRole.objects.get(pk=role_id)  # Update the TeamRole instance

        # Call any model method if needed
        # instance.model_method()

        # Update other fields in instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TeamDetailSerializers(serializers.ModelSerializer):
    """ Team details"""

    role = TeamRoleListSerializers(required=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'photo', 'role', 'date_create', 'date_update'
        ]
