import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import Story, db
import uuid

SIMPLE_CHARS = string.ascii_letters + string.digits
MAX_URL_LEN = 8
MAX_COOKIES_AGE = 60 * 60 * 24 * 7

app = Flask(__name__)
app.config.from_object('config')
db.app = app
db.init_app(app)
if not os.path.exists('stories.db'):
    db.create_all()


def get_random_url():
    return ''.join(random.choice(SIMPLE_CHARS) for char in range(MAX_URL_LEN))


def update_story(edited_story):
    stories = db.session.query(Story)
    story_to_update = stories.filter_by(story_url=edited_story['story_url'])
    for key, value in edited_story.items():
        if value is not '':
            story_to_update.update({key: value})
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def add_new_story():
    if request.method == 'POST':
        story_uid = str(uuid.uuid4())
        story_title = request.form.get('header')
        story_signature = request.form.get('signature')
        story_body = request.form.get('body')
        story_url = get_random_url()
        db.session.add(Story(story_url=story_url,
                             story_title=story_title,
                             story_signature=story_signature,
                             story_body=story_body,
                             story_uid=story_uid))
        db.session.commit()
        new_story = make_response(redirect(url_for('view_story',
                                                   story_url=story_url)))
        new_story.set_cookie('story_uid', story_uid, max_age=MAX_COOKIES_AGE)
        return new_story
    else:
        return render_template('form.html')


@app.route('/<story_url>')
def view_story(story_url):
    story_uid = request.cookies.get('story_uid')
    story = db.session.query(Story).get_or_404(story_url)
    return render_template('story.html', story=story, story_uid=story_uid)


@app.route('/edit/<story_url>', methods=['GET', 'POST'])
def edit_story(story_url):
    story_uid = request.cookies.get('story_uid')
    story_page = db.session.query(Story).get_or_404(story_url)
    if story_uid == story_page.story_uid:
        if request.method == 'POST':
            story_title = request.form.get('header')
            story_signature = request.form.get('signature')
            story_body = request.form.get('body')
            edited_story = {'story_title': story_title,
                            'story_signature': story_signature,
                            'story_body': story_body,
                            'story_url': story_page.story_url}
            update_story(edited_story)
        return render_template('form.html', story=story_page)
    else:
        return "You don't have permissions for edit this story!"


if __name__ == "__main__":
    app.run()
