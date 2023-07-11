FROM python:3.9

RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz -O /opt/node_exporter-1.6.0.linux-amd64.tar.gz
# RUN tar -xzf /opt/node_exporter-1.6.0.linux-amd64.tar.gz
RUN cd /opt && tar -xzf node_exporter-1.6.0.linux-amd64.tar.gz && rm node_exporter-1.6.0.linux-amd64.tar.gz

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /workspace
WORKDIR /workspace

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/workspace/entrypoint.sh"]
