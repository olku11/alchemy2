import flask
from data import db_session
from data.job import Jobs
from flask import jsonify
blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


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