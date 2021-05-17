FROM python


RUN mkdir /service

COPY protobufs/ /service/protobufs/

COPY src/ /service/src/

COPY templates/ /service/src/templates

WORKDIR /service/src

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/client.proto

ENV FLASK_APP /service/src/flask_client.py

EXPOSE 8080

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0", "--port", "8080"]
