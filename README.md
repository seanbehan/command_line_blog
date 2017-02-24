# Command Line Blog

Command Line Blog is a simple API for managing posts.

It is a Flask Blueprint that adds blog management to an existing Flask App. It assumes you will customize the
front end of the site and post display.

There is no web interface for managing your posts. All blogging is done by editing local files and uploading
them to your site using CURL (or other utility).

Make a POST request to the endpoint and it will perform an upsert. If there is already a post in the database at the path, it will update the content. If not, a new post will be created.

You can add attributes to your posts with headers, e.g., `-H 'Author: Sean'`. Header keys are snaked case. So you would
use `{{post.author}}` in your Jinja templates.

To edit an existing post, simply download the contents via curl to a local file. E.g.,

```
curl http://localhost/blog/hello-world > hello-world.md
```

Edit the contents and then upload the file back up to the server. E.g.,

```
curl -X POST http://localhost:5000/blog/hello-world -H 'Author: Sean' -F file=@hello-world.md
```

Example App that uses the command_line_blog module.

```python
from flask import Flask as App
from command_line_blog import command_line_blog as blog_app, command_line_blog_posts as posts

app = App(__name__)
app.register_blueprint(blog_app, url_prefix='/blog')

@app.route("/")
def index():
    return render_template('posts.html', posts=posts.all())

if __name__=='__main__':
    app.run(debug=True)
```

## How It Works

Dataset is used to manage the posts table so you don't have to define a schema in advance.

See docs for more info https://dataset.readthedocs.io/en/latest/index.html

## Configuration

The following environment variables should be set.

```
export DATABASE_URL = sqlite:///database.db
export COMMAND_LINE_BLOG_TABLE  = 'name_of_database_table'
export COMMAND_LINE_BLOG_USER   = 'username used for basic auth'
export COMMAND_LINE_BLOG_PWD    = 'password used for basic auth'
```
