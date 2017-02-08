FROM python:2.7
ADD . /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE True
RUN pip install -r requirements.txt