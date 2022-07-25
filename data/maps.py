import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy_serializer import SerializerMixin
from flask import Blueprint, jsonify


class Maps(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'maps'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_map = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    downoload_map = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)


maps_blueprint = Blueprint('maps_api', __name__,
                      template_folder='templates')


@maps_blueprint.route('/api/maps', methods=['GET'])
def get_maps():
    session = create_session()
    maps = session.query(Maps).all()
    return jsonify(
        {
            'maps':
                [item.to_dict() for item in maps]
        }
    )
