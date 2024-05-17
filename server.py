from flask import Flask

app = Flask(__name__)

@app.route("/")
def list_ideas():
  # TODO: actually display a list of ideas
  return 'todo'