from flask import render_template, url_for, flash, redirect
from app import app, db
import random
from app.forms import CreateArtistForm, LoginForm, RegistrationForm, CreateVenueForm, CreateEventForm
from app.models import Artist, Venue, Event, ArtistToEvent, User
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/base')
@login_required
def base():
    return render_template('base.html', title='Home')
'''
@app.route('/Artist')
def Artist():
    info = {
        "name": "Imagine Dragons",
        "hometown" : "Las Vegas",
        "artistDescription" : "a las vegas born band",
        "events": []
    }
    return render_template('Artist.html', info=info)
    '''
@app.route('/Artists')
def Artists():
    artists = Artist.query.all()

    return render_template('Artists.html', title='FavArtists', artists=artists)


@app.route('/artist/<name>')
def artist(name):
    info = Artist.query.filter_by(name=name).first()
    return render_template('Artist.html', title="Artist Information", info=info)


@app.route('/newArtist', methods=['GET', 'POST'])
def newArtist():

    form = CreateArtistForm()
    if form.validate_on_submit():
        a= Artist.query.filter_by(name=form.name.data).first()
        if a is not None:
            flash('Artist already exist')
        else:
            b = Artist(name=form.name.data, hometown=form.hometown.data)
            flash('New Artist Created!')
            db.session.add(b)
            db.session.commit()
            return redirect(url_for('Artists'))
    return render_template('newArtist.html',title="Create Artists", form=form)

@app.route('/newVenue', methods=['GET', 'POST'])
def newVenue():

    form = CreateVenueForm()
    if form.validate_on_submit():
        v= Venue.query.filter_by(name=form.name.data).first()
        if v is not None:
            flash('Venue already exists')
        else:
            w = Venue(name=form.name.data, address=form.address.data, city=form.city.data, state=form.state.data)
            flash('New Venue Created!')
            db.session.add(w)
            db.session.commit()
            return redirect(url_for('Artists'))
    return render_template('newVenue.html',title="Create Venues", form=form)

@app.route('/newEvent', methods=['GET', 'POST'])
def newEvent():

    form = CreateEventForm()
    form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
    form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]
    if form.validate_on_submit():
        e = Event.query.filter_by(name=form.name.data).first()
        if e is not None:
            flash('Event already exists')
        else:
            e = Event(name=form.name.data,date=form.date.data,
                      venueID=form.venue.data)
            flash('New Event Created!')
            db.session.add(e)
            db.session.commit()
            for aid in form.artists.data:
                a2e = ArtistToEvent(eventID=e.id,artistID=aid)
                db.session.add(a2e)
                db.session.commit()
            return redirect(url_for('Artists'))
    return render_template('newEvent.html',title="Create Events", form=form)
@app.route('/populate_db')
def populate_db():
    a1=Artist(name='Bastille', hometown="London")
    a2=Artist(name="Imagine Dragons", hometown="Las Vegas")
    a3=Artist(name="Of Monsters and Men", hometown="Reyjavik")
    v1=Venue(name="State Theater") #location="Downtown Ithaca")
    v2=Venue(name="A&ECenter") #location="IC")
    v3=Venue(name="Stewart Park") #location="Ithaca")
    v4=Venue(name="ICSquare") #location="IC")
    db.session.add_all([a1, a2, a3, v1, v2, v3, v4])
    db.session.commit()

    e1 =Event(name="IC Presents",venueID=v4.id,date=datetime(2020,8,6,17,30))
    e2 =Event(name="Rock the Park",venueID=v3.id,date=datetime(2020,8,6,17,30))
    e3 =Event(name="A&E Concerts",venueID=v2.id,date=datetime(2020,8,6,17,30))
    e4 =Event(name="State Theater Jam",venueID=v1.id,date=datetime(2020,8,6,17,30))
    e5 =Event(name="Music over Ithaca",venueID=v3.id,date=datetime(2020,8,6,17,30))
    db.session.add_all([e1,e2,e3,e4,e5])
    db.session.commit()

    AE1 = ArtistToEvent(eventID=e1.id, artistID=a3.id)
    AE2 = ArtistToEvent(eventID=e2.id, artistID=a2.id)
    AE3 = ArtistToEvent(eventID=e3.id, artistID=a1.id)
    AE4 = ArtistToEvent(eventID=e3.id, artistID=a2.id)
    db.session.add_all([AE1,AE2,AE3,AE4])
    db.session.commit()
    return "Database has been populated"

@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())
   db.session.commit()
   populate_db()
   return "Reset Database"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('Artists'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

