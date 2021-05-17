import csv
import random
import grpc
import youtube_videos_pb2_grpc
import youtube_videos_pb2

from flask import Flask
from concurrent import futures


app = Flask(__name__)


class VideoDataService(youtube_videos_pb2_grpc.VideoData):

    def ReceiveVideoData(self, request, context):
        with open('GBvideos.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                yield youtube_videos_pb2.YoutubeVideoData(video_id=row[0], trending=row[1], title=row[2], channel_title=row[3], category=int(row[4]),
                                                  publish_time=row[5], tags=row[6], views=int(row[7]), likes=int(row[8]),
                                                  dislikes=int(row[9]), comment_count=int(row[10]), thumbnail_link=row[11], comments_disabled=bool(row[12]),		
                                                  ratings_disabled=bool(row[13]), video_error_or_removed=bool(row[14]), description=row[15])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    youtube_videos_pb2_grpc.add_VideoDataServicer_to_server(
        VideoDataService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

