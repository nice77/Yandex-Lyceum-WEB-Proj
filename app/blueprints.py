from flask import Blueprint, jsonify, make_response, request

from app.models import *
from app import db

jobs = Blueprint('jobs_api', __name__, template_folder='templates')


@jobs.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Unexpected job_id datatype'}), 404)


@jobs.route('/api/jobs', methods=['GET', 'POST'])
def get_jobs():
    if request.method == 'POST':
        values = dict(map(lambda x: (x[0], x[1]), request.form.items()))
        if Jobs.query.filter_by(id=int(values['id'])).first():
            return jsonify({'error': 'Id already exists'})
        to_add = Jobs(**dict(map(lambda x: (x[0], x[1]), request.form.items())))
        db.session.add(to_add)
        db.session.commit()
        return 'Added'
    if request.method == 'GET':
        a = list(map(lambda x: x.__dict__, Jobs.query.all()))
        for i in a:
            i.pop('_sa_instance_state', None)
        return jsonify({'jobs': a})


@jobs.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    a = Jobs.query.filter_by(id=job_id).first()
    if not a:
        return jsonify({'error': 'Job_id not found'})
    a = a.__dict__
    a.pop('_sa_instance_state', None)
    return jsonify({'job': a})


@jobs.route('/api/jobs_delete', methods=['POST'])
def delete_job():
    job = Jobs.query.filter_by(id=int(request.form['id'])).first()
    print(job)
    if job:
        db.session.delete(job)
        db.session.commit()
        return 'Done'
    else:
        return jsonify({'error': 'Job not found'})
