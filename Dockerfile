FROM python:3.12

WORKDIR /usr/src/app
COPY oil.py oil_multiple.py requirements.txt ./
RUN chmod +x oil.py oil_multiple.py
RUN apt-get update --yes && apt-get install --yes xvfb chromium && pip install -r requirements.txt

CMD ["python", "/usr/src/app/oil_multiple.py"]
