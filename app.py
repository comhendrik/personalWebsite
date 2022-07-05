import os
import json

from flask import * 

from db import get_db, query_db, init_app

import json

# create and configure the app
IMAGE_FOLDER = os.path.join('static', 'images')
app = Flask(__name__, instance_relative_config=True, template_folder='templates', static_folder='static')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE='db.sqlite',
    UPLOAD_FOLDER = IMAGE_FOLDER
)


try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/index')
def direct_to_index():
    return render_template("index.html")

@app.route('/about')
def direct_to_about():
    return render_template("about.html")

@app.route('/cv')
def direct_to_cv():
    f = open('data/cv.json')
    data = json.load(f)
    f.close()
    return render_template("cv.html", cv_data = data)

@app.route('/blog')
def direct_to_blog():
    db = get_db()
    cursor = db.cursor()
    results = query_db("SELECT * FROM article", cursor=cursor)
    results = sorted(results, key=lambda d: d['id'], reverse=True)
    db.close()
    return render_template("blog.html", article=results)

@app.route('/portfolio')
def direct_to_portfolio():
    f = open('data/portfolio.json')
    data = json.load(f)
    f.close()
    return render_template("portfolio.html", portfolio_data = data)

@app.route('/<int:article_id>')
def direct_to_blog_article(article_id):
    db = get_db()
    cursor = db.cursor()
    results = query_db(f"SELECT * FROM article WHERE id={article_id}", cursor=cursor)
    db.close()
    if len(results) == 0:
        return render_template("404.html")
    return render_template("article.html", article=results[0])


init_app(app)


from adminData import admin

app.register_blueprint(admin.bp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
