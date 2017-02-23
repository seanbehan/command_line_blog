import re
from os import environ as env
from datetime import datetime
from flask import Blueprint, request, g, jsonify
from dataset import connect

command_line_blog = Blueprint('command_line_blog', __name__)

@command_line_blog.before_request
def before_request():
    g.db = connect(env.get('DATABASE_URL', 'sqlite:///database.db'))

@command_line_blog.route('/<slug>')
def show_post_path(slug):
    post = g.db['posts'].find_one(slug=slug)
    if post:
        return post['body']
    else:
        return "Not found"

@command_line_blog.route("/all.json")
def show_all_posts():
    return jsonify(posts=[row for row in g.db.query('select * from posts')])

@command_line_blog.route('/<slug>.json')
def show_post_json_path(slug):
    return jsonify(g.db['posts'].find_one(slug=slug))

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

    g.db['posts'].upsert(row, ['slug'])

    return jsonify(row)

@command_line_blog.route("/<slug>/", methods=["DELETE"])
def delete_post_path(slug):
    g.db['posts'].delete(g.db['posts'].find_one(slug=slug))
    return "Deleted"
