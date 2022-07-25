import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy_serializer import SerializerMixin
from flask import Blueprint, jsonify, request

class Records(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'records'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    map_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User', back_populates='records')


records_blueprint = Blueprint('records_api', __name__,
                      template_folder='templates')


@records_blueprint.route('/api/records/<int:record_id>', methods=['GET'])
def get_one_record(record_id):
    session = create_session()
    record = session.query(Records).get(record_id)
    if not record:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'record': record.to_dict(only=('id', 'map_name', 'points', 'user_id'))
        }
    )


@records_blueprint.route('/api/records/<name>', methods=['GET'])
def get_record(name):
    session = create_session()
    records = session.query(Records).filter(Records.map_name == name)
    if not records:
        return jsonify({'records': False})
    return jsonify(
        {
            'records':
                [item.to_dict(only=('id', 'map_name', 'points', 'user_id'))
                 for item in sorted(records, key=lambda x: x.points, reverse=True)]
        }
    )


@records_blueprint.route('/api/records', methods=['POST'])
def create_record():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['map_name', 'points', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    record = Records(
        map_name=request.json['map_name'],
        points=request.json['points'],
        user_id=request.json['user_id']
    )
    session.add(record)
    session.commit()
    return jsonify({'success': 'OK'})


@records_blueprint.route('/api/records/<int:record_id>', methods=['GET', 'POST'])
def transform_one_record(record_id):
    session = create_session()
    record = session.query(Records).get(record_id)
    if not record:
        return jsonify({'error': 'Not found'})
    for key in ['map_name', 'points', 'user_id']:
        if key in request.json.keys():
            exec('record.{}={}'.format(key, request.json[key]))
    session.commit()
    return jsonify({'success': 'OK'})


@records_blueprint.route('/api/records/<int:job_id>', methods=['DELETE'])
def delete_record(record_id):
    session = create_session()
    record = session.query(Records).get(record_id)
    if not record:
        return jsonify({'error': 'Not found'})
    session.delete(record)
    session.commit()
    return jsonify({'success': 'OK'})
