from flask import Blueprint, render_template, abort
from simpledu.models import User, Course

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def user_index(username):
    user = User.query.filter_by(username=username).first()
    if user:
        names = Course.query.filter_by(author=user).all()
        return render_template('user.html', user=user, names=names)
    else:
        abort(404)
