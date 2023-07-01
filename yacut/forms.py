from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class YacutForm(FlaskForm):
    """Класс формы и валидаторы полей форм для модели URLMap."""
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256),
                    URL(require_tld=True, message='Ссылка некорректна')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Regexp(regex=r'^[A-Za-z0-9]+$',
                           message='Допустимы только латинские буквы и цифры'),
                    Length(1, 16, message='Ссылка не должна превышать 16 символов'),
                    Optional()]
    )
    submit = SubmitField('Создать')
