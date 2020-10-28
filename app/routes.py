from flask import render_template, url_for, flash, redirect
from app import app, db
import random
from app.forms import CreateArtistForm
from app.models import Artist, Venue, Event, ArtistToEvent

@app.route('/')
@app.route('/base')
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

    e1 =Event(name="IC Presents",venueID=v4.id)
    e2 =Event(name="Rock the Park",venueID=v3.id)
    e3 =Event(name="A&E Concerts",venueID=v2.id)
    e4 =Event(name="State Theater Jam",venueID=v1.id)
    e5 =Event(name="Music over Ithaca",venueID=v3.id)
    db.session.add_all([e1,e2,e3,e4,e5])
    db.session.commit()

    AE1 = ArtistToEvent(eventID=e1.id, artistID=a3.id)
    AE2 = ArtistToEvent(eventID=e2.id, artistID=a2.id)
    AE3 = ArtistToEvent(eventID=e3.id, artistID=a1.id)
    AE4 = ArtistToEvent(eventID=e3.id, artistID=a2.id)
    db.session.add_all([AE1,AE2,AE3,AE4])
    db.session.commit()

    '''
    e1=Event(name="Rock the State", venueID=v1.id)
    e2=Event(name="A&E Concerts", venueID=v2.id)
    e3=Event(name="A Night at the Park", venueID=v3.id)
    e4=Event(name="IC Presents", venueID=v4.id)
    e5 = Event(name="Rock out Ithaca", venueID=v4.id)
    db.session.add_all([e1,e2,e3,e4,e5])
    db.session.commit()
    '''
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


