from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///index.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text_article = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/articles')
def articles():
    posts = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", articles=posts)


@app.route('/articles/<int:id>')
def show_article(id):
    article = Article.query.get(id)
    return render_template("each_article.html", article=article)


@app.route('/articles/<int:id>/delete')
def delete_article(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/articles/<int:id>/update', methods=["POST", "GET"])
def update_article(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text_article = request.form['text_article']

        try:
            db.session.commit()
            return redirect('/articles')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("update_article.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text_article = request.form['text_article']

        article = Article(title=title, intro=intro, text_article=text_article)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/articles')
        except:
            return 'При добавлении статьи вышла ошибка!'
    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run()
