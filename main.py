from flask import Flask, render_template, abort
from jinja2.exceptions import TemplateNotFound
from apscheduler.schedulers.background import BackgroundScheduler
from news import top_headlines
from waitress import serve

sched = BackgroundScheduler(daemon=True)
# sched.add_job(top_headlines,'interval',minutes=30)
sched.start()

top_headlines()
app = Flask('app')

# ctrl + shift + R to reload cached static files but doesn't seem to be necessary with replit
@app.route('/')
def hello_world(name=None):
  return render_template('index.html', name=name)

@app.route('/banking/')
@app.route('/banking/<path:path>')
def banking(path=None):
    try:
        return render_template(f"banking/{path or 'index'}.html")
    except TemplateNotFound:
        try:
            return render_template(f"banking/{path}")
        except TemplateNotFound:
            return abort(404)

@app.route('/investment/')
@app.route('/investment/<path:path>')
def investment(path=None):
    try:
        return render_template(f"investment/{path or 'index'}.html")
    except TemplateNotFound:
        try:
            return render_template(f"investment/{path}")
        except TemplateNotFound:
            return abort(404)
        

serve(app, host="0.0.0.0", port=8080)
