FROM python:3.11

WORKDIR /Parts_Warehouse_API

COPY . /Parts_Warehouse_API

RUN pip install -r requirements.txt

EXPOSE 8000

ENV SECRET_KEY = 'Django secret key'
ENV MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
ENV DATABASE_NAME = 'Database name'

ENV TEST_MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
ENV TEST_DATABASE_NAME = 'Test database name'

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
