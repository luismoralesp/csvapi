from dynamic_models.models import ModelSchema, FieldSchema
import pandas 
import concurrent.futures
from django.conf import settings
from django.db import connection

class Service:
  def process_file(name, file):
    chunksize = settings.CHUNK_SIZE
    chunklist = pandas.read_csv (file, chunksize=chunksize)
    create_model_thread = None
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)

    def worker(data, i):
      """thread worker function"""

      # wait for table creation
      model = create_model_thread.result()

      try:
        # prepare data for bulk_create
        data = [ model( **{ 
          Service.fix(key): value 
          for key, value in row.items() 
        }) for row in data ]

        model.objects.bulk_create(data)
        connection.close()
      except Exception as e:
        print (i, e)

    def create_model(data):
      fields = list(data[0].keys())
      model = Service.new_model(name, fields)
      connection.close()
      return model

    threads = []
    for chunk in chunklist:
      # get data from chunk
      data = chunk.to_dict('records')

      # append thread for create model before use it
      if not create_model_thread:
        create_model_thread = executor.submit(create_model, data)
        threads.append(create_model_thread)

      # thread for process this data chunk
      thread = executor.submit(worker, data, len(threads))
      threads.append(thread)
    
    for thread in threads:
      thread.result()

  def fix(key):
    return key.strip().lower().replace(' ', '_').replace('.', '')

  def get_model(name):
    obj = ModelSchema.objects.filter(name=name).first()
    if obj:
      return obj.as_model()
    
  def new_model(name, fields):
    schema = ModelSchema.objects.create(name=name)
    for field in fields:
      FieldSchema.objects.create(
          name=field,
          data_type='character',
          model_schema=schema, 
          max_length=255,  
      )
    return schema.as_model()
