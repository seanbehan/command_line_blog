WIP - Todos

- Needs authentication
- Customize table name

# Command Line Blog

Command Line Blog is a simple Flask Blueprint that adds blog management to your Flask App. It assumes you will customize the
front end of the site and post display, using Jinja/Flask.

There is no web interface for managing your posts, however. All blogging is done by editing local files and uploading
them to your site via CURL (or other utility).

You simply make a POST request to the endpoint and it will perform an upsert. If there is already a post with the slug in the database, it will update the content. If not, a new post will be created.

You can add attributes to your posts with headers, e.g., `-H 'Author: Sean'`. Header keys are snaked case. So you would
use `{{post.author}}` in your Jinja templates.

To edit an existing post, simply download the contents via curl to a local file. E.g.,

```
curl http://localhost/blog/hello-world > hello-world.md
```

Edit the contents and then upload the file back up to the server. E.g.,

```
curl -X POST http://localhost:5000/blog/hello-world` -H 'Author: Sean' -F file=@hello-world.md
```

Example App that uses the command_line_blog module.

```python
from flask import Flask as App
from command_line_blog import command_line_blog as blog

app = App(__name__)
app.register_blueprint(blog, url_prefix='/blog')

@app.route("/")
def index():
    return "Hello World"

if __name__=='__main__':
    app.run(debug=True)
```

## How It Works

Dataset is used to manage posts table so you don't have to define a schema in advance.

## Database Connection

It assumes `DATABASE_URL` is set as an environment variable. Otherwise it defaults to an in memory SQLite database. 
