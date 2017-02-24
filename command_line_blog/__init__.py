import re
from os import environ as env
from datetime import datetime
from flask import Blueprint, request, g, jsonify, Response as response
from dataset import connect

command_line_blog = Blueprint('command_line_blog', __name__)
command_line_blog_db = lambda: connect(env.get('DATABASE_URL', 'sqlite:///:memory:'))

@command_line_blog.before_request
def before_request():
    g.db = command_line_blog_db()
    g.posts = g.db[env.get('COMMAND_LINE_BLOG_TABLE', 'command_line_blog_posts')]

@command_line_blog.before_request
def require_authorized_user():
    username, password = env.get('COMMAND_LINE_BLOG_USER', None), env.get('COMMAND_LINE_BLOG_PWD', None)
    auth = request.authorization
    if not auth or (auth.username != username or auth.password != password):
        return response('Authentication required.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@command_line_blog.route('/<slug>/')
def show_post_path(slug):
    post = g.posts.find_one(slug=slug)
    if post:
        return post['body']
    else:
        return "Not found"

@command_line_blog.route("/all.json")
def show_all_posts():
    return jsonify({
        env.get('COMMAND_LINE_BLOG_TABLE', 'command_line_blog_posts') : [row for row in g.posts.all()]
    })

@command_line_blog.route('/<slug>.json')
def show_post_json_path(slug):
    return jsonify(g.posts.find_one(slug=slug))

@command_line_blog.route("/<slug>/", methods=["POST"])
def create_post_path(slug):
    row = dict(
        update=datetime.utcnow(),
        slug=slug
    )
    for key, value in request.headers.items():
        key = re.sub('\W+', '_', key).strip('_').lower()
        row[key] = value
    if request.files.get('file', None):
        row['body'] = request.files['file'].read()

    g.posts.upsert(row, ['slug'])

    return jsonify(row)

@command_line_blog.route("/<slug>/", methods=["DELETE"])
def delete_post_path(slug):
    g.posts.delete(g.posts.find_one(slug=slug))
    return "Deleted"
