# change the version probably...
FROM python:3.9

# review if we need all of these things
RUN pip install pandas sqlalchemy psycopg2 fastparquet pyarrow

WORKDIR /app
#COPY ingest_data.py ingest_data.py

#ENTRYPOINT [ "python", "ingest_data.py" ]
ENTRYPOINT [ "python" ]