from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Feedback
from . import db

auth = Blueprint('auth', __name__)
loopResult = ""

@auth.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        feedbackText = request.form.get('feedbackText')

        print(email, firstName, feedbackText)

        user = Feedback.query.filter_by(email=email).first()
        if user:
            flash('Feedback already submitted!', category='error')
            return redirect(url_for("auth.feedback"))
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) <2:
            flash('First Name must be at least 2 characters.', category='error')
        else:
            new_feedback = Feedback(email=email, firstName=firstName, feedbackText=feedbackText)
            db.session.add(new_feedback)
            db.session.commit()

            flash('Feedback submitted!', category='success')

    return render_template("feedback.html")
