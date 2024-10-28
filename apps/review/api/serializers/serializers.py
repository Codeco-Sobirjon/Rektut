from rest_framework import serializers

from apps.review.models import *
from apps.ads.models import Job


class ReviewListSerializers(serializers.ModelSerializer):
    """ Review create update and details """
    job = serializers.IntegerField(required=True)
    rating = serializers.IntegerField(max_value=5, min_value=1, write_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'job', 'user', 'rating', 'description', 'first_name', 'email',
            'date_create', 'date_update'
        ]
        read_only_fields = ('date_created',)

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class ReviewDetailSerializers(serializers.ModelSerializer):
    """ Review details create update and details """
    job = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'job', 'user', 'rating', 'description', 'first_name', 'email',
            'date_create', 'date_update'
        ]

    def get_job(self, obj):
        """ get job title. type : str """
        return Job.objects.filter(id=obj.job.id).values('title')

    def get_user(self, obj):
        """
        get user details
            {
                "email" : "test@test.com",
                "phone" : "+9989912345678",
                ...
            }
        """
        return list(CustomUser.obejcts.filter(id=obj.user.id).values(
            'id', 'email', 'phone', 'first_name', 'last_name', 'photo'
        ))