import random
import string

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import YacutForm
from yacut.models import URLMap


def get_unique_short_id():
    """Формирование коротких идентификаторов."""
    while True:
        short_id = ''.join(
            random.choices(string.ascii_letters, k=6)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция для главной страницы."""
    form = YacutForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!', 'error-message')
            custom_id = None
            return render_template('index.html', form=form)
        elif custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()

        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        flash(url_for('yacut_redirect', short_id=custom_id, _external=True), 'link-message')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def yacut_redirect(short_id):
    """View-функция, отвечающая за переадресацию."""
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is not None:
        original_link = urlmap.original
        return redirect(original_link)
    abort(404)
