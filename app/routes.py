from flask import render_template, url_for
from app import app
import random

@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html', title='Home')

@app.route('/Artist')
def Artist():
    return render_template('Artist.html')

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

@app.route('/newArtist')
def newArtist():
    return render_template('newArtist.html')

