from flask import render_template, request, session, flash, redirect, url_for
from blog.forms import LoginForm
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
import functools


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))

    return check_permissions


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/<int:entry_id>/", methods=["GET", "POST"])
@app.route("/post/", methods=["GET", "POST"], defaults={"entry_id": None})
@login_required
def post(entry_id):
    if entry_id:
        entry = Entry.query.get_or_404(entry_id)
    else:
        entry = Entry(is_published=True)

    form = EntryForm(obj=entry)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(entry)
        if not entry_id:
            db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("entry_form.html", form=form, entry_id=entry_id)

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


@app.route("/delete-post/<int:entry_id>", methods=['POST'])
@login_required
def delete_entry(entry_id):
    post = Entry.query.get_or_404(entry_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted.', 'success')
    return redirect(url_for('index'))
