from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Story(db.Model):
    story_slug = db.Column(db.String(32), primary_key=True)
    story_uid = db.Column(db.String(128))
    story_title = db.Column(db.String(64))
    story_signature = db.Column(db.String(128))
    story_body = db.Column(db.Text)
    author_id = db.Column(db.String(64))
