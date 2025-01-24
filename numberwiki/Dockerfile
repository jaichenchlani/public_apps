FROM --platform=linux/amd64 python:3.7-alpine
# FROM python:3.7-alpine
WORKDIR /main
COPY . /main
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]