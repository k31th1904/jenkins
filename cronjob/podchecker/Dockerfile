FROM bitnami/kubectl as kubectl
FROM python:3.8-slim
COPY --from=kubectl /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/
RUN apt update
RUN pip install kubernetes
RUN apt install -y vim
RUN mkdir /app
COPY run.py /app
WORKDIR /app
CMD for i in $(seq 1 6); do python run.py; sleep 10; done
