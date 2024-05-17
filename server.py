import collections
import flask
import sqlite3

import main

app = flask.Flask(__name__)

db_key = '_database'

def get_db():
  db = getattr(flask.g, db_key, None)
  if db is None:
    db = flask.g._database = sqlite3.connect(main.db_filename)
  return db

@app.teardown_appcontext
def close_connection(_e):
  db = getattr(flask.g, db_key, None)
  if db is not None:
    db.close()

Idea = collections.namedtuple('Idea', 'id idea count')

@app.route("/add-idea", methods=['post'])
def add_idea():
  db = get_db()
  db.execute('insert into ideas (idea, count) values (?, 1);', [flask.request.form['idea']])
  db.commit()
  return flask.redirect('/')

@app.route("/bump-idea", methods=['post'])
def bump_idea():
  db = get_db()
  db.execute('update ideas set count = count + 1 where id = ?;', [flask.request.form['id']])
  db.commit()
  return flask.redirect('/')

@app.route("/")
def list_ideas():
  cursor = get_db().cursor()
  query = cursor.execute('select id, idea, count from ideas order by count desc').fetchall()
  ideas = []
  for (id, idea, count) in query:
    ideas.append(Idea(id, idea, count))
  cursor.close()
  return flask.render_template('ideas.html', ideas=ideas)
