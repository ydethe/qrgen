from flask import render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields import SubmitField


class MyForm(FlaskForm):
    url = StringField("url", validators=[DataRequired()])
    submit = SubmitField("Générer")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # index page
    @app.route("/", methods=("GET", "POST"))
    def index():
        form = MyForm()
        if form.validate_on_submit():
            # return redirect('/success')
            print(form.url)
        return render_template("index.html", form=form)

    return app


# waitress-serve --port 3566 --call 'qrgen.compute:create_app'
