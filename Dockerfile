FROM  python:3.6.10-slim
RUN apt-get -y update && apt-get install -y libzbar-dev

RUN pip3 install cryptography==2.7 \
requests==2.18.4 \
Cython==0.28.2 \
pandas==0.23.0 \
numpy==1.17.0 \
setuptools==41.2.0 \
psutil==5.4.5 \
scipy==1.1.0 \
minepy==1.2.4 \
python_graph_core==1.8.2 \
scikit_learn==0.21.3 \
PyYAML==5.1.2 \
matplotlib==3.2.1 \
biopython==1.76

COPY . /
