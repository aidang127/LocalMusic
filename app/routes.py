from flask import render_template, url_for, flash
from app import app
import random
from app.forms import CreateArtistForm

@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html', title='Home')

@app.route('/Artist')
def Artist():
    info = {
        "artistName": "Imagine Dragons",
        "hometown" : "Las Vegas",
        "artistDescription" : "a las vegas born band",
        "events": []
    }
    return render_template('Artist.html', info=info)
@app.route('/Artists')
def Artists():
    artists = [
        {'name': 'Imagine Dragons'},
        {'name': 'Bastille'},
        {'name': 'Of Monsters and Men'},
        {'name': 'AJR'},
        {'name': 'Fitz and the Tantrums'}
    ]
    return render_template('Artists.html', title='FavArtists', artists=artists)

@app.route('/newArtist', methods=['GET', 'POST'])
def newArtist():
    form = CreateArtistForm()
    if form.validate_on_submit():
        flash('New Artist Created: {}'.format(form.artistName.data))
        new_form = CreateArtistForm()
        info = {}
        info ["artistName"] = form.artistName.data
        info["hometown"] = form.hometown.data
        info["artistDescription"] = form.artistDescription.data
        info["events"] = []

        return render_template('Artist.html', info=info)
    return render_template('newArtist.html',title="Create Artists", form=form)
