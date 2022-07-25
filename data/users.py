from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from .db_session import SqlAlchemyBase, orm, create_session
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import datetime
from flask import Blueprint, jsonify


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(15), unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    records = orm.relation("Records", back_populates='user')
    news = orm.relation("News", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

user_blueprint = Blueprint('user_api', __name__,
                      template_folder='templates')


@user_blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'name': user.to_dict(only=('id', 'name'))
        }
    )


@user_blueprint.route('/api/user', methods=['GET'])
def get_users():
    session = create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name')) for item in users]
        }
    )
