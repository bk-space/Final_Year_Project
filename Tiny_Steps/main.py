from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import BlogPost, TripPlan
from . import db
import os
from datetime import datetime
import stripe

main = Blueprint("main", __name__)

stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@main.route('/')
def index():
    blogs = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(4).all()

    return render_template("index.html", title="Home", blogs=blogs)

@main.route('/blogs', methods=['GET', 'POST'])
def blogs():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        pic.save(os.path.join(os.path.dirname(__file__), 'static/posts', filename))

        blog = BlogPost(date_posted=datetime.now(), title=title, content=content, pic=pic.read(), pic_name=filename, mimetype=mimetype, tourist=current_user)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, int)
    blogs = BlogPost.query.paginate(page=page, per_page=6)
    
    return render_template("blogs.html", title="Blogs", blogs=blogs)

@main.route('/blogs/<int:id>')
def blogpost(id):
    post = BlogPost.query.filter_by(id=id).first()
    return render_template("blogpost.html", post=post)

@main.route('/about')
def aboutus():
    return render_template("about_us.html", title="About")

@main.route('/adventure')
def adventure():
    transport = request.args.get('transport', 'All', str)
    page = request.args.get('page', 1, int)

    if transport == 'Ship' or transport == 'Plane' or transport == 'Train':
        plans = TripPlan.query.filter(TripPlan.transport == transport).paginate(page=page, per_page=10)
    else:
        plans = TripPlan.query.paginate(page=page, per_page=10)

    return render_template("adventure.html", title="Adventures", plans=plans)

@main.route('/pay')
def payment():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1KudJISD2iC3vN8tB0LPD6f2',
            'quantity': 1
        }],
        mode='payment',
        success_url=url_for('main.index', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.index', _external=True)
    )

    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': current_app.config['STRIPE_PUBLIC_KEY']
    }

@main.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Gallery")