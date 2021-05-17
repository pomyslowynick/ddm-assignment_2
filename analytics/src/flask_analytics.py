import time
import random
import math
import logging
import nltk
import grpc
from nltk.sentiment import SentimentIntensityAnalyzer
from analytics_pb2_grpc import PostsServiceStub, AnalyticsServicer, add_AnalyticsServicer_to_server, VideoDataStub
from analytics_pb2 import PostRequest, PostStats, DeletedStats, VideoStats, VideoDataRequest, StatsData, RankedVideo
from flask import Flask, render_template, jsonify
from concurrent import futures

app = Flask(__name__)


def filter_last_3_minutes_posts(posts_list, current_time):
    return [d for d in posts_list if d['time'] > (current_time - 180)]


def get_sentiment(title):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(title)
    if sentiment_score["compound"] > 0:
        return "positive"
    else:
        return "negative"


def run():
    with grpc.insecure_channel('flask-server:50051', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = PostsServiceStub(channel)
        for response in stub.ReceivePosts(PostRequest(id=1)):
            time.sleep(random.randint(0, 1))
            print("Analytics client received: " + response.id, flush=True)
            yield response


def getVideoData():
    with grpc.insecure_channel('flask-video-server:50053', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = VideoDataStub(channel)
        for response in stub.ReceiveVideoData(VideoDataRequest(id=1)):
            time.sleep(random.randint(0, 1))
            print("Analytics client received: " + response.video_id, flush=True)
            yield response


class AnalyticsService(AnalyticsServicer):
    def __init__(self):
        self.total_posts = 0
        self.highest_scored_post = 0
        self.average_score_3_minutes = 0
        self.posts_last_3_minutes = []
        self.removed_posts_stats = {
            "moderator": 0, "reddit": 0, "automod_filtered": 0, "deleted": 0}
        self.most_disliked_video = {"dislikes": -1}
        self.most_liked_video = {"likes": -1}
        self.posts_response_iterator = run()
        self.video_data_response_iterator = getVideoData()
        self.total_videos = 0
        self.comments_split = {"moreThan1000": 0, "lessThan1000": 0}
            
    def ReceiveAnalytics(self, request, context):
        for post, video in zip(self.posts_response_iterator, self.video_data_response_iterator):
            self.total_videos += 1
            self.total_posts += 1
            current_time = time.time()
            self.posts_last_3_minutes.append(
                {"time": current_time, "score": post.score})

            self.posts_last_3_minutes = filter_last_3_minutes_posts(
                self.posts_last_3_minutes, current_time)

            # Get an average score for last 3 minutes
            if self.posts_last_3_minutes:
                self.average_score_3_minutes = round(float(sum(
                    post["score"] for post in self.posts_last_3_minutes)) / len(self.posts_last_3_minutes), 2)

            # Get the highest scoring post
            if post.score > self.highest_scored_post:
                self.highest_scored_post = post.score

            # Get the most disliked video so far
            if video.dislikes > self.most_disliked_video["dislikes"]:
                self.most_disliked_video = {"title": video.title, "dislikes": video.dislikes}
            
            # Get the most liked video so far
            if video.likes > self.most_liked_video["likes"]:
                self.most_liked_video = {"title": video.title, "likes": video.likes}

            # Get the sentiment for video and post
            post_sentiment = get_sentiment(post.title)
            video_sentiment = get_sentiment(video.description)

            # Update video comments split
            if video.comment_count > 1000:
                self.comments_split["moreThan1000"] += 1
            else:
                self.comments_split["lessThan1000"] += 1

            # Updated the remove_by stats
            if post.removed_by:
                if post.removed_by in self.removed_posts_stats:
                    self.removed_posts_stats[post.removed_by] += 1
                else:
                    self.removed_posts_stats[post.removed_by] = 1

            most_disliked_video=RankedVideo(score=self.most_disliked_video["dislikes"], title=self.most_disliked_video["title"])
            most_liked_video=RankedVideo(score=self.most_liked_video["likes"], title=self.most_liked_video["title"])

            video_stats = VideoStats(total_videos=self.total_videos, description_sentiment=video_sentiment, most_disliked_video=most_disliked_video, most_liked_video=most_liked_video, comment_count_more_than_1000=self.comments_split["moreThan1000"],  comment_count_less_than_1000=self.comments_split["lessThan1000"], video=video)
            
            deleted_stats = DeletedStats(moderator=self.removed_posts_stats["moderator"], reddit=self.removed_posts_stats["reddit"], deleted=self.removed_posts_stats["deleted"], automod_filtered=self.removed_posts_stats["automod_filtered"])
            
            post_stats = PostStats(total_posts=self.total_posts, average_score=self.average_score_3_minutes, highest_rated_post=self.highest_scored_post, post_sentiment=post_sentiment, post=post, delete_stats=deleted_stats)
            
            yield StatsData(post_stats=post_stats, video_stats=video_stats)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AnalyticsServicer_to_server(
        AnalyticsService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
