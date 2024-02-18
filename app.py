from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)


# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    experience = db.Column(db.String(200))
    skills = db.Column(db.String(200))
    interests = db.Column(db.String(200))


class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    mission_statement = db.Column(db.Text)
    offerings = db.Column(db.String(200))
    team_members = db.Column(db.String(200))
    investors = db.Column(db.String(200))
    partners = db.Column(db.String(200))
    pitch_deck_url = db.Column(db.String(200))


# Define forms
class RegistrationForm(FlaskForm):
    username = StringField('Username')
    experience = StringField('Experience')
    skills = StringField('Skills')
    interests = StringField('Interests')


class StartupForm(FlaskForm):
    name = StringField('Name')
    description = TextAreaField('Description')
    mission_statement = TextAreaField('Mission Statement')
    offerings = StringField('Offerings')
    team_members = StringField('Team Members')
    investors = StringField('Investors')
    partners = StringField('Partners')
    pitch_deck_url = URLField('Pitch Deck URL')
    submit = SubmitField('Create Startup')


# Dummy data for illustration purposes
# ...


@app.route('/')
def home():
    users = User.query.all()
    startups = Startup.query.all()
    return render_template('index.html', users=users, startups=startups)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            experience=form.experience.data,
            skills=form.skills.data,
            interests=form.interests.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/startups/<startup_id>', methods=['GET', 'POST'])
def startup_profile(startup_id):
    startup = Startup.query.get(int(startup_id))
    if not startup:
        return redirect(url_for('home'))

    form = StartupForm(obj=startup)

    if form.validate_on_submit():
        form.populate_obj(startup)
        db.session.commit()

    return render_template('startup_profile.html', startup=startup, form=form)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)


# Define database models
# ... (User and Startup models from previous example)

class MentorshipProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.String(50), nullable=False)
    founder_name = db.Column(db.String(50), nullable=False)
    expertise = db.Column(db.String(200), nullable=False)
    availability = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ...


@app.route('/mentorship', methods=['GET', 'POST'])
def mentorship():
    form = MentorshipProgramForm()
    
    if form.validate_on_submit():
        mentorship_program = MentorshipProgram(
            mentor_name=form.mentor_name.data,
            founder_name=form.founder_name.data,
            expertise=form.expertise.data,
            availability=form.availability.data,
            message=form.message.data
        )
        db.session.add(mentorship_program)
        db.session.commit()

    mentorship_programs = MentorshipProgram.query.all()
    return render_template('mentorship.html', form=form, mentorship_programs=mentorship_programs)


class MentorshipProgramForm(FlaskForm):
    mentor_name = StringField('Mentor Name')
    founder_name = StringField('Founder Name')
    expertise = StringField('Expertise')
    availability = StringField('Availability')
    message = TextAreaField('Message')
    submit = SubmitField('Submit')

# ...


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)


# Define database models
# ... (User, Startup, MentorshipProgram models from previous examples)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ...


@app.route('/follow/<entity_type>/<int:entity_id>')
def follow(entity_type, entity_id):
    user_id = 1  # replace with actual user ID (you might use Flask-Login for authentication)

    if entity_type == 'user':
        followed_user = User.query.get(entity_id)
        follow_entity(user_id, followed_user.id, None)
    elif entity_type == 'startup':
        followed_startup = Startup.query.get(entity_id)
        follow_entity(user_id, None, followed_startup.id)

    return redirect(url_for('home'))


def follow_entity(follower_id, followed_user_id, followed_startup_id):
    follow = Follow(
        follower_id=follower_id,
        followed_user_id=followed_user_id,
        followed_startup_id=followed_startup_id
    )
    db.session.add(follow)
    db.session.commit()


# ...


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
