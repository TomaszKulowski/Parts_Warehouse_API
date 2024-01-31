FROM python:3.11

WORKDIR /Parts_Warehouse_API

COPY . /Parts_Warehouse_API

RUN pip install -r requirements.txt

EXPOSE 8000

ENV SECRET_KEY="django-insecure-qi*5y5#v&3iwt1-zbwdr!*@5o5-8x1=0-f)h0()lgdvu8ynp"
ENV MONGO_CONNECTION_STR="mongodb+srv://tomek987125:fcw3Kj0bthuaEueU@tomasz.1jkibvn.mongodb.net/?retryWrites=true&w=majority"
ENV DATABASE_NAME="tom"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
