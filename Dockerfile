FROM python:3.8
WORKDIR /eikon
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "app.py"]
EXPOSE 5500