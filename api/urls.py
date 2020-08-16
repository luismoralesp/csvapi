from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'@/(?P<model>.+)', views.DynamicModelViewSet, basename='dynamicmodel')
router.register(r'csvdocument', views.CsvDocumentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]