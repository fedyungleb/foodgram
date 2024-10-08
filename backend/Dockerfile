FROM python:3.8.5

WORKDIR /code

COPY requirements.txt .
COPY .env /code/foodgram/

RUN python3 -m pip install pip==22.2.2
RUN pip install -r requirements.txt
RUN pip install django-colorfield



COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000