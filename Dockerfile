FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./apt_src_aliyun /etc/apt/sources.list

RUN apt-get update

RUN apt-get install -y --no-install-recommends python3.7 python3.7-dev python3-distutils python3-pip && apt-get autoremove
RUN cd /usr/bin && ln -sf python3.7 python && ln -sf python3.7 python3 && ln -sf pip3 pip && python -m pip install --upgrade pip
# RUN pip --no-cache-dir install numpy pandas sklearn pyyaml easydict keras==2.3.1 h5py==2.10.0 tensorflow==1.15 Flask
RUN pip --no-cache-dir install numpy pandas sklearn pyyaml easydict keras==2.3.1 h5py==2.10.0 tensorflow==1.15 Flask -i https://mirrors.aliyun.com/pypi/simple/

RUN apt-get install -y --no-install-recommends git && apt-get autoremove

RUN pip --no-cache-dir install xiangqi

ENV WORKSPACE /workspace
ENV CODE_DIR $WORKSPACE/src
ENV PYTHONPATH $CODE_DIR
COPY ./src $CODE_DIR
COPY ./scripts/self_play.sh $WORKSPACE/self_play.sh
RUN chmod +x $WORKSPACE/self_play.sh
RUN bash -c "mkdir -p $WORKSPACE/logs"

VOLUME  $WORKSPACE/data

WORKDIR $WORKSPACE

# CMD self_play.sh
