# CsvAPI

## Requirements

* Python 3.8.5
* PostgreSQL 12.3

## Install

Clone repository:

```bash
$ git clone https://github.com/luismoralesp/csvapi.git
$ cd csvapi
```

Install dependeces:
```bash
$ pip install -r requirements.txt
```

Copy enviroment file example:
```bash
$ cp csvapi/.env_example csvapi/.env
```

Set value for variable 
* `DATABASE_URL`
  
for more info see this [link](https://django-environ.readthedocs.io/en/latest/).

Set value for variables:
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_STORAGE_BUCKET_NAME`

for more info see this [guide](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html).


Run this command for create tables in database:
```bash
$ python manage migrate
```

Run this command for upload media to S3:
```bash
$ python manage collectstatics
```

## Run

```bash
$ python manage runserver
```

## Test

```bash
$ python manage test
```