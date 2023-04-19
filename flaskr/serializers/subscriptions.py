from serializers import ma


class SubscriptionSchema(ma.Schema):
    class Meta:
        fields = ("__all__", )
