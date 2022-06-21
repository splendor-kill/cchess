FROM ubuntu:18.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./apt_src_aliyun /etc/apt/sources.list

RUN apt-get update

RUN apt-get install -y --no-install-recommends git python3.7 python3.7-dev python3.7-distutils python3-pip && apt-get autoremove
RUN cd /usr/bin && ln -sf python3.7 python && ln -sf python3.7 python3 && ln -sf pip3 pip && python -m pip install --upgrade pip

RUN pip install numpy pandas scikit-learn pyyaml easydict pyperclip keras==2.3.1 h5py==2.10.0 tensorflow==1.15 -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install --upgrade "protobuf<=3.20.1" -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install xiangqi minio

ENV WORKSPACE /workspace
ENV CODE_DIR $WORKSPACE/src
ENV PYTHONPATH $CODE_DIR
COPY ./src $CODE_DIR
SHELL ["/bin/bash", "-c"]
RUN echo $'#!/bin/bash\n\
PYTHONUNBUFFERED=1 python src/main.py --cmd $1 src/config.yaml > $1.log 2>&1 &\
' > $WORKSPACE/run.sh
RUN chmod +x $WORKSPACE/run.sh
RUN bash -c "mkdir -p $WORKSPACE/logs"
RUN bash -c "mkdir -p $WORKSPACE/data/play_data"
RUN bash -c "mkdir -p $WORKSPACE/data/model/next_generation"

VOLUME  $WORKSPACE/data

WORKDIR $WORKSPACE

CMD ["./run.sh self"]
