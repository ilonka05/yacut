from http import HTTPStatus
from re import match

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id

VALID_CHARACTERS = r'^[A-Za-z0-9]+$'
MAX_LENGTH_CUSTOM_ID = 16


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or data['url'] == '':
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    elif not match(VALID_CHARACTERS, data['custom_id']) or len(data['custom_id']) > MAX_LENGTH_CUSTOM_ID:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_urlmap(short_id):
    """GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору."""
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK
