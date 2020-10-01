from core.models import Person, CheckIn, IssueDetail
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
    
    def create(self, validated_data):
        employee = Person.objects.create(**validated_data)
        return employee

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance
    
