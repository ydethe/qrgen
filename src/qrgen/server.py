import io

import logfire
from PIL import Image
from flask import render_template, Flask, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields import SubmitField
import qrcode

from . import settings


class MyForm(FlaskForm):
    url = StringField("url", validators=[DataRequired()])
    size = IntegerField("size", default=10, validators=[DataRequired()])
    submit = SubmitField("Générer")


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    logfire.instrument_flask(app)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
    )

    # Index page
    @app.route("/", methods=("GET", "POST"))
    def index():
        form = MyForm()
        if form.validate_on_submit():
            qr = qrcode.QRCode(
                version=int(form.size.data),
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=10,
                border=4,
            )
            qr.add_data(form.url.data)
            qr.make(fit=False)
            img = qr.make_image(fill_color="black", back_color="white")
            fp = io.BytesIO()
            format = Image.registered_extensions()[".png"]
            img.save(fp, format)
            fp.seek(0)
            return send_file(
                fp, mimetype="image/png", as_attachment=True, download_name="qrcode.png"
            )

        return render_template("index.html", form=form)

    return app


# waitress-serve --port 3566 --call 'qrgen.server:create_app'
