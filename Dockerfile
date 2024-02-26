FROM python:3.11

WORKDIR /Parts_Warehouse_API

COPY . /Parts_Warehouse_API

RUN pip install -r requirements.txt

EXPOSE 8000

SECRET_KEY = 'Django secret key'
MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
DATABASE_NAME = 'tom'

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
