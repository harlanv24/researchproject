from rest_framework import serializers

class ArxivResultSerializer(serializers.Serializer):
    # Define the fields you want to serialize
    title = serializers.CharField(max_length=200)
    summary = serializers.CharField()
    # Add other fields as needed
