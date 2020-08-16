from django.test import TestCase
from rest_framework.test import APIRequestFactory
from . import views

import random
import string
from io import BytesIO

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_csv():
  columns = random.randint(5, 10)
  rows = 5000
  data = ''

  for row in range(rows):
    array = [ get_random_string(10) for col in range(columns) ]
    data += ','.join(array) + '\n'
  return BytesIO(str.encode(data))

# Create your tests here.
class TestApi(TestCase):
  def test_api(self):
    factory = APIRequestFactory()
    name = get_random_string(8)

    print ("Checking CsvDocument API [POST]...")
    request = factory.post('/csvdocument/', { 
      'name': name,
      'file': get_csv()
    })
    view = views.CsvDocumentViewSet.as_view({'post': 'create'})
    response = view(request).render()

    assert response.status_code == 201

    print ("Checking CsvDocument API [GET]...")
    request = factory.get('/csvdocument/')
    view = views.CsvDocumentViewSet.as_view({'get': 'list'})
    response = view(request).render()
    
    assert response.status_code == 200

    print ("Checking DynamicModel API [GET]...")
    request = factory.get('/dynamicmodel/@/' + name)
    view = views.DynamicModelViewSet.as_view({'get': 'list'})
    response = view(request, model=name).render()

    assert response.status_code == 200
    assert len(response.data['results']) <= 10

