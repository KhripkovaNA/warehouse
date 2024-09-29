FROM python:3.11

RUN mkdir /warehouse

WORKDIR /warehouse

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/app.sh