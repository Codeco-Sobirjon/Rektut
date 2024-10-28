from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.ads.models import *


class CategoryListSerializers(serializers.ModelSerializer):
    """ Category create update and details """
    icon = serializers.ImageField(required=False)
    name = serializers.CharField(required=True)
    subcategory = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'subcategory', 'icon', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CategoryDetailSerializers(serializers.ModelSerializer):
    """ Category  details """
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'subcategory', 'icon', 'date_create', 'date_update'
        ]

    def get_subcategory(self, obj):
        if obj.subcategory is None:
            return obj.subcategory
        return CategoryDetailSerializers(obj.subcategory).data


class CountryListSerializers(serializers.ModelSerializer):
    """ Country create update and details """
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class CityListSerializers(serializers.ModelSerializer):
    """ City create update and details """

    class Meta:
        model = City
        fields = [
            'id', 'name', 'country', 'short_name', 'date_create', 'date_update'
        ]

    def create(self, validated_data):
        return super().create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_method()
        return super().update(instance, validated_data)


class CitySerializer(serializers.ModelSerializer):
    country = CountryListSerializers(read_only=True)

    class Meta:
        model = City
        fields = [
            'id', 'name', 'country', 'short_name', 'date_create', 'date_update'
        ]


class OptionalFieldListSerializers(serializers.ModelSerializer):

    class Meta:
        model = OptionalField
        fields = ['id', 'name', 'key', 'type', 'is_required', 'default', 'max_length',
                  'min_length', 'is_active']


class OptionalFieldThroughListSerializers(serializers.ModelSerializer):
    job = serializers.IntegerField(required=True)
    image = serializers.ImageField(required=False)
    file = serializers.FileField(required=True)

    class Meta:
        model = OptionalFieldThrough
        fields = [
            'id', 'job', 'optional_field', 'value', 'image', 'file'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class OptionalFieldThroughDetailSerializers(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    optional_field = OptionalFieldListSerializers(read_only=True)
    class Meta:
        model = OptionalFieldThrough
        fields = [
            'id', 'job', 'optional_field', 'value', 'image', 'file'
        ]

    def get_job(self, obj):
        return obj.job.title


class JobListSerializers(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    additionally = serializers.JSONField(required=True, write_only=True)  # Mark as write-only

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'category', 'city', 'description', 'contact_number',
            'email', 'name', 'photo', 'date_create', 'date_update',
            'additionally',
        ]

    def create(self, validated_data):
        """
        create job additionally
        [
            {
                "optionalFieldID": 1,
                "value": "something to write",
                "image": "image send",
                "file": "file send"
            }, ...
        ]
        """
        user = self.context.get('request').user
        additionally = validated_data.pop('additionally', [])
        job_instance = Job.objects.create(**validated_data, user=user)
        for item in additionally:
            optional_field_id = item.get('optionalFieldID')
            try:
                optional_field_instance = OptionalField.objects.get(id=optional_field_id)
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"optionalFieldID": f"Invalid OptionalField ID: {optional_field_id}"})
            OptionalFieldThrough.objects.create(
                job=job_instance,
                optional_field=optional_field_instance,
                value=item.get('value'),
                image=item.get('image'),
                file=item.get('file')
            )
        return job_instance

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        additionally_data = validated_data.pop('additionally', [])

        # Update the Job instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user = user  # Assuming you want to update the user as well
        instance.save()

        # Process the additionally data
        if additionally_data:
            existing_ids = [item['id'] for item in additionally_data if 'id' in item]
            for item in additionally_data:
                if 'id' in item and OptionalFieldThrough.objects.filter(id=item['id']).exists():
                    # Update existing OptionalFieldThrough instance
                    optional_instance = OptionalFieldThrough.objects.get(id=item['id'])
                    optional_instance.value = item.get('value', optional_instance.value)
                    optional_instance.image = item.get('image', optional_instance.image)
                    optional_instance.file = item.get('file', optional_instance.file)
                    optional_instance.save()
                else:
                    # Create new OptionalFieldThrough instance
                    optional_field_id = item.get('optionalFieldID')
                    try:
                        optional_field_instance = OptionalField.objects.get(id=optional_field_id)
                    except ObjectDoesNotExist:
                        raise serializers.ValidationError(
                            {"optionalFieldID": f"Invalid OptionalField ID: {optional_field_id}"})
                    OptionalFieldThrough.objects.create(
                        job=instance,
                        optional_field=optional_field_instance,
                        value=item.get('value'),
                        image=item.get('image'),
                        file=item.get('file')
                    )

            # Delete OptionalFieldThrough instances that were not included in the update
            if existing_ids:
                instance.optionallyfieldthrough_set.exclude(id__in=existing_ids).delete()

        return instance


class JobDetailSerializers(serializers.ModelSerializer):
    """ Job details create update and details """
    optional_field = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'category', 'city', 'description', 'contact_number',
            'email', 'name', 'user', 'status', 'photo', 'date_create', 'date_update',
            'is_top', 'is_vip', 'optional_field'
        ]

    def get_category(self, obj):
        """ get job category. type : str """
        return obj.category.name

    def get_city(self, obj):
        """
        get city type. type : list
            {
                "name" : "Barcelona",
                "country": "Spain"
            }
        """
        return list(City.objects.filter(id=obj.city.id).values('name', 'country'))[0]

    def get_user(self, obj):
        """
        get user details
            {
                "email" : "test@test.com",
                "phone" : "+9989912345678",
                ...
            }
        """
        return list(CustomUser.objects.filter(id=obj.user.id).values(
            'id', 'email', 'phone', 'first_name', 'last_name', 'photo'
        ))[0]

    def get_optional_field(self, obj):
        optional_fields = OptionalFieldThrough.objects.filter(job=obj)
        data = OptionalFieldThroughDetailSerializers(optional_fields, many=True).data
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if 'user' in representation and 'photo' in representation['user']:
            logo_path = representation['user']['photo']
            if logo_path and request:
                representation['user']['photo'] = request.build_absolute_uri(logo_path)
        return representation
