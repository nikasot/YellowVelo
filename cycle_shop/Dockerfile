FROM python:latest

WORKDIR /django_app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN pip install cloudipsp==1.0.3
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["/django_app/entrypoint.sh"]
