FROM python:3.10-alpine
WORKDIR /app
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY app.py .
COPY connect_to_TMDB.py .
COPY connect_to_mongoDB.py .
COPY templates templates/
CMD [ "python", "app.py" ]


