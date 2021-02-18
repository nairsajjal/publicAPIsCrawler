FROM python:3

ADD crawler.py /
COPY . /
WORKDIR /
RUN pip3 install -r dependencies.txt
CMD [ "python3", "./crawler.py"]