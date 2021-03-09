import datetime
import io
import json
import os

from flask import Flask, render_template, request, redirect, Response, send_file, abort

app = Flask(__name__)


@app.route('/')
def index():
    age = int((datetime.date.today() - datetime.date(1995, 4, 22)).days / 365)
    return render_template('home.html', age=age)




@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")['projects']

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', projects=data, tag=tag)


@app.route('/projects/<title>')
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('404.html'), 404
    else:
        selected = in_project


    # load html if the json file doesn't contain a description
    link = selected['link']
    f = f'static/projects/{link}/{link}.html'
    selected['description'] = io.open(get_static_file(f), "r", encoding="utf-8").read()
    return render_template('project.html', project=selected)


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))





if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
