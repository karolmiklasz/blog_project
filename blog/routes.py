from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/<int:entry_id>/", methods=["GET", "POST"])
@app.route("/post/", methods=["GET", "POST"], defaults={"entry_id": None})
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
