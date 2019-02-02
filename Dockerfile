FROM python
ENV PYTHONBUFFERED 1
RUN mkdir /src
ADD . /src
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt
