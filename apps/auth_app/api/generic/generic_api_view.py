from rest_framework import mixins, viewsets


class CommonAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
     Base class for processing API requests. (Class for defining new methods)
     """

     # Dictionary with serializers for request and response.
     # Example: {'create': {'request': Serializer, 'response': Serializer}}
     # Defaults to serializer_class
    SERIALIZER = {}
    lookup_field = "id"


class GenericAPIView(CommonAPIView):
    """
     Class for processing API requests. (Class for overriding DRF methods)
     """

    def get_serializer_class(self):
        """Returns the serializer class for the request"""

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.action not in self.SERIALIZER:
            return self.serializer_class

        return self.SERIALIZER.get(self.action).get("request", self.serializer_class)

    def get_serializer_response(self, instance, **kwargs) -> dict:
        """Returns a serialized object"""

        if self.action not in self.SERIALIZER:
            return self.serializer_class(instance, **kwargs).data

        return self.SERIALIZER.get(self.action).get("response", self.serializer_class)(instance, **kwargs).data
