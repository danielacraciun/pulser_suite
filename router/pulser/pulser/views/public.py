# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from base64 import standard_b64encode

from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app,session)
import datetime

from flask_login import login_user, login_required, logout_user

from pulser.extensions import login_manager
from pulser.models.user import User
from pulser.forms.public import LoginForm
from pulser.forms.user import RegisterForm
from pulser.utils import flash_errors, render_extensions
from pulser.database import db
from .api import client_id, client_secret, token_url
from requests_oauthlib import OAuth2Session


blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.profile")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_extensions("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               email=form.email.data,
                               password=form.password.data,
                               active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_extensions('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_extensions("public/about.html", form=form)

@blueprint.route('/robots.txt')
@blueprint.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])

@blueprint.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """
    Generate sitemap.xml. Makes a list of urls and date modified.
    """
    pages = []
    ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
    ten_days_ago = ten_days_ago.date().isoformat()
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, ten_days_ago])

    sitemap_xml = render_template('public/sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@blueprint.route("/callback", methods=["GET"])
def callback():
    """ Step 2: Retrieving an access token.
    """
    pair_as_bytes = "{}:{}".format(client_id, client_secret).encode('utf-8')
    pair = standard_b64encode(pair_as_bytes).decode('utf-8')
    oauth_session = OAuth2Session(client_id, scope=['heartrate'], redirect_uri="localhost:5000/callback")
    token = oauth_session.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url,
       headers={'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Authorization': 'Basic {}'.format(pair),
    })

    session['oauth_token'] = token
    return redirect(url_for('.hr'))