FROM python

ENV NLTK_DATA /service/src/nltk_data

RUN mkdir /service

COPY protobufs/ /service/protobufs/

COPY src/ /service/src/

WORKDIR /service/src


RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/analytics.proto

RUN python -m nltk.downloader vader_lexicon

EXPOSE 50052

ENTRYPOINT [ "python", "flask_analytics.py" ]
