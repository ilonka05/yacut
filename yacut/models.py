from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Описание модели URLMap."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Метод для сериализации объектов класса в словарь."""
        return dict(
            url=self.original,
            short_link=url_for('yacut_redirect', short_id=self.short, _external=True)
        )

    def from_dict(self, data):
        """Метод-десериализатор для добавления в пустой объект класса значения полей,
        полученных в POST-запросе.
        """
        self.original = data['url']
        self.short = data['custom_id']
