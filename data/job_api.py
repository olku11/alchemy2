import flask
from data import db_session
from data.job import Jobs
from flask import jsonify
from flask import Flask
from flask import make_response


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


app = Flask(__name__)

@blueprint.route('/api/jobs')
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
    if not jobs:
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

