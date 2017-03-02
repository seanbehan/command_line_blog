import re
from os import environ as env
from datetime import datetime
from flask import Blueprint, request, jsonify, Response as response
from dataset import connect

command_line_blog = Blueprint('command_line_blog', __name__)
command_line_blog_db = connect(env.get('DATABASE_URL', 'sqlite:///:memory:'))
command_line_blog_posts = command_line_blog_db()[env.get('COMMAND_LINE_BLOG_TABLE', 'command_line_blog_posts')]

@command_line_blog.before_request
def require_authorized_user():
    username, password = env.get('COMMAND_LINE_BLOG_USER', None), env.get('COMMAND_LINE_BLOG_PWD', None)
    auth = request.authorization
    if not auth or (auth.username != username or auth.password != password):
        return response('Authentication required.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@command_line_blog.route('/<slug>')
def show_post_path(slug):
    post = command_line_blog_posts.find_one(slug=slug)
    if post:
        return post['body']
    else:
        return "Not found"

@command_line_blog.route("/<slug>", methods=["POST"])
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

    command_line_blog_posts.upsert(row, ['slug'])
    return jsonify(row)

@command_line_blog.route("/<slug>", methods=["DELETE"])
def delete_post_path(slug):
    command_line_blog_posts.delete(command_line_blog_posts.find_one(slug=slug))
    return "Deleted"
