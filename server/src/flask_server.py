import csv
import random
import grpc
import reddit_posts_pb2_grpc
import reddit_posts_pb2

from flask import Flask
from concurrent import futures


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"


class PostService(reddit_posts_pb2_grpc.PostsServiceServicer):

    def ReceivePosts(self, request, context):
        with open('r_dataisbeautiful_posts.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                yield reddit_posts_pb2.RedditPost(id=row[0], title=row[1], score=int(row[2]), author=row[3], author_flair_text=row[4],
                                                  removed_by=row[5], total_awards_received=float(row[6]), awarders=row[7], created_utc=row[8],
                                                  full_link=row[9], num_comments=int(row[10]), over_18=bool(row[11]))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_posts_pb2_grpc.add_PostsServiceServicer_to_server(
        PostService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

