from flask import Blueprint, render_template
import pickle

site = Blueprint('site', __name__)


@site.route('/')
def index():
    return render_template('home.jinja')


@site.route('/about')
def about():
    return render_template('about.jinja')


@site.route('/test')
def test():
    return render_template('test.jinja')


@site.route('/result', methods=['GET', 'POST'])
def result():
    asd_model = pickle.load(open('app/static/asd_model.pkl', 'rb'))

    return render_template('result.jinja')
