from rest_framework import serializers

class AnimalSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=127)
    address = serializers.CharField(max_length=255)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    image = serializers.ImageField()
    
