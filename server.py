import os
import random
import string
import uuid
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import Story, db


SIMPLE_CHARS = string.ascii_letters + string.digits
MAX_URL_LEN = 8
MAX_COOKIES_AGE = 60 * 60 * 24 * 7

app = Flask(__name__)
app.config.from_object('config')
db.app = app
db.init_app(app)
if not os.path.exists('stories.db'):
    db.create_all()


def get_random_slug():
    return ''.join(random.choice(SIMPLE_CHARS) for char in range(MAX_URL_LEN))


def update_story(edited_story):
    stories = db.session.query(Story)
    story_to_update = stories.filter_by(story_slug=edited_story['story_slug'])
    story_to_update.update(edited_story)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def add_new_story():
    if request.method == 'POST':
        author_id = request.cookies.get('cookie')
        if not author_id:
            author_id = str(uuid.uuid4())
        story_uid = str(uuid.uuid4())
        story_title = request.form.get('header')
        story_signature = request.form.get('signature')
        story_body = request.form.get('body')
        story_slug = get_random_slug()
        db.session.add(Story(story_slug=story_slug,
                             story_title=story_title,
                             story_signature=story_signature,
                             story_body=story_body,
                             story_uid=story_uid,
                             author_id=author_id))
        db.session.commit()
        new_story = make_response(redirect(url_for('view_story',
                                                   story_slug=story_slug)))
        new_story.set_cookie('author_id', author_id, max_age=MAX_COOKIES_AGE)
        return new_story
    else:
        return render_template('form.html')


@app.route('/<story_slug>')
def view_story(story_slug):
    author_id = request.cookies.get('author_id')
    story = db.session.query(Story).get_or_404(story_slug)
    return render_template('story.html', story=story, author_id=author_id)


@app.route('/edit/<story_slug>', methods=['GET', 'POST'])
def edit_story(story_slug):
    author_id = request.cookies.get('author_id')
    story_page = db.session.query(Story).get_or_404(story_slug)
    if author_id == story_page.author_id:
        if request.method == 'POST':
            story_title = request.form.get('header')
            story_signature = request.form.get('signature')
            story_body = request.form.get('body')
            edited_story = {'story_title': story_title,
                            'story_signature': story_signature,
                            'story_body': story_body,
                            'story_slug': story_page.story_slug}
            update_story(edited_story)
        return render_template('form.html', story=story_page)
    else:
        return "You don't have permissions for edit this story!"


if __name__ == "__main__":
    app.run()
