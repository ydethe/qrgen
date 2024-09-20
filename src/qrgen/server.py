import io
import typing as T

import logfire
from PIL import Image
from flask import render_template, Flask, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, ColorField
from wtforms.validators import DataRequired
from wtforms.fields import SubmitField
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    RoundedModuleDrawer,
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask

from . import settings, logger


style_choices = {
    "SquareModuleDrawer": SquareModuleDrawer,
    "RoundedModuleDrawer": RoundedModuleDrawer,
    "CircleModuleDrawer": CircleModuleDrawer,
    "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
    "HorizontalBarsDrawer": HorizontalBarsDrawer,
    "VerticalBarsDrawer": VerticalBarsDrawer,
}
correction_choices = {
    "l": qrcode.constants.ERROR_CORRECT_L,
    "m": qrcode.constants.ERROR_CORRECT_M,
    "q": qrcode.constants.ERROR_CORRECT_Q,
    "h": qrcode.constants.ERROR_CORRECT_H,
}


class CodeConfigurationForm(FlaskForm):
    url = StringField(label="Donnée du QR code", validators=[DataRequired()])
    size = IntegerField(label="Taille", default=10, validators=[DataRequired()])
    back_color = ColorField(label="Couleur d'arrière-plan", default="#FFFFFF")
    fill_color = ColorField(label="Couleur de remplissage", default="#000000")
    style = SelectField(
        label="Style",
        choices=[
            ("SquareModuleDrawer", "Carrés"),
            ("RoundedModuleDrawer", "Arrondi"),
            ("CircleModuleDrawer", "Cercle"),
            ("GappedSquareModuleDrawer", "Carrés disjoints"),
            ("HorizontalBarsDrawer", "Barres horizontales"),
            ("VerticalBarsDrawer", "Barres verticales"),
        ],
        default="SquareModuleDrawer",
    )
    correction = SelectField(
        label="Correction d'erreur",
        choices=[
            ("l", "Bas"),
            ("m", "Moyen"),
            ("q", "Bonne qualité"),
            ("h", "Haute qualité"),
        ],
        default="m",
    )
    submit = SubmitField("Générer")


def color_str_to_tuple(col: str) -> T.Tuple[int]:
    col_t = [int(col[x : x + 2], 16) for x in (1, 3, 5)]
    return tuple(col_t)


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
        form = CodeConfigurationForm()
        if form.validate_on_submit():
            code_data = form.url.data
            code_size = int(form.size.data)

            style_cls = style_choices[form.style.data]
            correction = correction_choices[form.correction.data]
            back_color = color_str_to_tuple(form.back_color.data)
            fill_color = color_str_to_tuple(form.fill_color.data)

            logger.info(f"Generating code for '{code_data}")

            qr = qrcode.QRCode(
                version=code_size,
                error_correction=correction,
                box_size=10,
                border=4,
            )
            qr.add_data(code_data)
            qr.make(fit=False)
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=style_cls(),
                color_mask=SolidFillColorMask(back_color=back_color, front_color=fill_color),
            )
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
