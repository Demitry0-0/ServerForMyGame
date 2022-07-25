import datetime
import sqlalchemy
from sqlalchemy import orm
from flask import Blueprint, jsonify, request
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='Сообщение')
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')


news_blueprint = Blueprint('news_api', __name__,
                      template_folder='templates')


@news_blueprint.route('/api/news')
def get_news():
    session = create_session()
    news = session.query(News).all()
    if not news:
        return jsonify({'news': False})
    return jsonify(
        {
            'news':
                news[-1].to_dict(only=('title', 'content', 'user.name', 'created_date'))
        }
    )


@news_blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    session = create_session()
    news = session.query(News).all()
    if not 0 < news_id <= len(news):
        return jsonify({'news': False})
    return jsonify(
        {
            'news': news[news_id - 1].to_dict(only=('title', 'content',
                                                    'user.name', 'created_date'))
        }
    )


@news_blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id']
    )
    session.add(news)
    session.commit()
    return jsonify({'success': 'OK'})


@news_blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    session = create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    session.delete(news)
    session.commit()
    return jsonify({'success': 'OK'})
