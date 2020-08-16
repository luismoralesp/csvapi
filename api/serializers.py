from rest_framework import serializers
from .models import CsvDocument
from django.urls import reverse
from .services import Service

class HyperlinkedRelatedFieldDynamicModel(serializers.HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        args = [ obj, ]
        return request.build_absolute_uri(reverse(view_name, args=args ))


class DynamicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
    

class CsvDocumentSerializer(serializers.ModelSerializer):
    url = HyperlinkedRelatedFieldDynamicModel(
        read_only=True,
        view_name='dynamicmodel-list',
        source='name'
    )

    def create(self, validated_data):
        request = self.context.get("request")
        file = request.FILES.get('file')
        name = request.POST.get('name')
        Service.process_file(name, file)
        return super().create(validated_data)


    class Meta:
        model = CsvDocument
        fields = '__all__'