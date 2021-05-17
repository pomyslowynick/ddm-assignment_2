import grpc, time, random, logging, requests, json
from google.protobuf import json_format
from client_pb2_grpc import AnalyticsStub
from client_pb2 import PostRequest
from flask import Flask, render_template, jsonify
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)

PrometheusMetrics(app)

def run():
    with grpc.insecure_channel('flask-analytics:50052', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = AnalyticsStub(channel)
        for response in stub.ReceiveAnalytics(PostRequest(id=1)):
            yield response



@app.route('/')
def hello_world():
    return render_template('index.html', data=run())

analytics_response = run()

@app.route('/get_data')
def get_data():
    response = next(analytics_response)

    post = response.post_stats
    clean_post_title = remove_profanities_text(post.post.title)

    encoded_post = {"title": clean_post_title, "score": post.post.score, "total_posts":post.total_posts, "average_score_3_minutes": round(post.average_score, 2), "highest_scored_post": post.highest_rated_post, "post_sentiment":post.post_sentiment, "delete_stats": {"moderator": post.delete_stats.moderator, "deleted": post.delete_stats.deleted, "automod_filtered": post.delete_stats.automod_filtered, "reddit": post.delete_stats.reddit}}

    video = response.video_stats
    clean_video_title = remove_profanities_text(video.video.title)
    
    encoded_video = {"total_videos": video.total_videos, "description_sentiment": video.description_sentiment, "title": clean_video_title, "views": video.video.views, "comment_count_more_than_1000": video.comment_count_more_than_1000, "comment_count_less_than_1000": video.comment_count_less_than_1000, "most_disliked_video": {"dislikes": video.most_disliked_video.score, "title": video.most_disliked_video.title}, "most_liked_video": {"likes": video.most_liked_video.score, "title": clean_video_title}}

    return jsonify({"encoded_post": encoded_post, "encoded_video": encoded_video})

@app.route('/get_clean')
def get_clean_test_call():
    sample_description = json.dumps({"description": "This post is shit :("})
    response = requests.post(url='http://profanity-checker.default.svc.cluster.local:8080', data=sample_description, json=sample_description)
    return response.content

def remove_profanities_text(text):
    try:
        sample_description = json.dumps({"description": text})
        response = requests.post(url='http://profanity-checker.default.svc.cluster.local:8080', data=sample_description, json=sample_description)
        assert(response.status_code == 200)
        processed_response = json.loads(response.content)
        print(processed_response)
        return processed_response["censoredDescription"]
    except:
        print("Serverless function is not working, defaulting to provided title.")
        return text