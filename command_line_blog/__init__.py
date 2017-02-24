import re
from os import environ as env
from datetime import datetime
from flask import Blueprint, request, g, jsonify
from dataset import connect

class CommandLineBlogBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        self.table_space = kwargs.pop('table_space', 'command_line_blog_posts')
        Blueprint.__init__(self, *args, **kwargs)

command_line_blog = CommandLineBlogBlueprint('command_line_blog', __name__)

@command_line_blog.before_request
def before_request():
    g.db = connect(env.get('DATABASE_URL', 'sqlite:///:memory:'))
    g.posts = g.db[command_line_blog.table_space]

@command_line_blog.route('/<slug>')
def show_post_path(slug):
    post = g.posts.find_one(slug=slug)
    if post:
        return post['body']
    else:
        return "Not found"

@command_line_blog.route("/all.json")
def show_all_posts():
    return jsonify({
        command_line_blog.table_space : [row for row in g.posts.all()]
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
