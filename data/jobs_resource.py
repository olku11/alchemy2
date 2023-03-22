from flask_restful import Resource
from data import db_session
from data.job import Jobs
from flask import abort, jsonify
from data.jobs_parse import parser
import datetime as dt


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(job_id)
    if not news:
        abort(404, description=f'Job {job_id} not found.')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'jobs': job.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        return jsonify({'out': 'Нет функции put'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs()
        job.team_leader = args['team_leader']
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.start_date = dt.datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
        job.end_date = dt.datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
        job.is_finished = args['is_finished']
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})