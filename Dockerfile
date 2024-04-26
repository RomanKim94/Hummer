FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python -m pip install -r requirements.txt
