FROM python


RUN mkdir /service

COPY proto/ /service/proto/

COPY src/ /service/src/

WORKDIR /service/src

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../proto --python_out=. --grpc_python_out=. ../proto/youtube_videos.proto


EXPOSE 50053

ENTRYPOINT [ "python", "flask_video_server.py" ]
