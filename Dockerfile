FROM ubuntu:22.04

WORKDIR /usr/src/app 

RUN apt-get update && apt-get install build-essential wget tar -y
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -xzf ta-lib-0.4.0-src.tar.gz
RUN cd ta-lib/

RUN sudo ./configure
RUN sudo make
RUN sudo make install && cd ..

RUN pip install ta-lib
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./main.py .

CMD ["main.py"]
ENTRYPOINT ["python3"]