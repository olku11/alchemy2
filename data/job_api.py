import flask
from data import db_session
from data.job import Jobs
from flask import jsonify
from flask import Flask
from flask import make_response
from flask import request
import datetime as dt

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)

app = Flask(__name__)


@blueprint.route('/api/jobs', methods=['GET'])
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date",
                                    "is_finished")) for item in news]
        }
    )


@blueprint.route('/api/jobs/<job_id>', methods=['GET'])
def get_one_news(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)

    if not job_id.isdigit():
        return jsonify({'error': 'not int'})
    elif not jobs:
        return jsonify({'error': 'No id'})
    return jsonify(
        {
            'jobs': jobs.to_dict(
                only=('id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date",
                      "is_finished"))
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["id", 'team_leader', 'job', 'work_size', 'collaborators', "start_date", "end_date", "is_finished"]):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(request.json['id'])
    if news:
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs()
    jobs.id = request.json['id']
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.start_date = dt.datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S')
    jobs.end_date = dt.datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S')
    jobs.is_finished = request.json['is_finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})