from .models import CsvDocument
from rest_framework import viewsets
from rest_framework import status
from django.http import JsonResponse
from .serializers import DynamicModelSerializer, CsvDocumentSerializer

class DynamicModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows DynamicModel to be viewed or edited.
    """
    serializer_class = DynamicModelSerializer
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = '__all__'
    ordering = ('-id')

    def dispatch(self, request, *args, **kwargs):
        self.csv = CsvDocument.objects.filter(name=self.kwargs['model']).first()
        if self.csv:
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({'error': 'This api is not implemented yet'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return self.csv.get_model().objects.all()

    def get_serializer_class(self):
        DynamicModelSerializer.Meta.model = self.csv.get_model()
        return DynamicModelSerializer 

class CsvDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CsvDocument to be viewed or edited.
    """
    queryset = CsvDocument.objects.all().order_by('-id')
    serializer_class = CsvDocumentSerializer
    ordering_fields = '__all__'
    search_fields = '__all__'
    ordering = ['-id']