import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, send_file
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from info import gmail, receiver, password, subject, secret_key
from names import names



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


app = Flask(__name__)



app.config['SECRET_KEY'] = secret_key
ckeditor = CKEditor(app)
Bootstrap5(app)


class ReviewForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    room = StringField("Room", validators=[DataRequired()])
    table = StringField("Table", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    rate = SelectField("Rate", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], validators=[DataRequired()])
    submit = SubmitField("Send!")

class RateStaffForm(FlaskForm):
    staff_name = StringField("Staff Name", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    rate = SelectField("Rate", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], validators=[DataRequired()])
    submit = SubmitField("Send!")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")
@app.route("/staff_appreciation")
def staff_appreciation():
    return render_template("staff_appreciation.html")

@app.route("/port_activities")
def port_activities():
    return render_template("port_activities.html")

@app.route("/e_card")
def e_card():
    return render_template("e_card.html")

@app.route("/Our Values")
def values():
    return render_template("values.html")

@app.route("/Service")
def service():
    return render_template("service.html")

@app.route("/bolaji_AFSS_e_card")
def bolaji_AFSS_e_card():
    return render_template("bolaji_AFSS_e_card.html")

@app.route("/bolaji_NASO_bussines_card")
def bolaji_NASO_bussines_card():
    return render_template("bolaji_NASO_bussines_card.html")

@app.route("/training")
def training():
    return render_template("training.html")


@app.route('/Company_Profile')
def view_pdf():
    # Path to PDF file
    pdf_path = 'static/AFSS_Profile_.pdf'

    # Send the PDF file with the correct headers
    return send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=False,
        download_name='file.pdf'
    )


@app.route("/csr_projects")
def csr_projects():
    return render_template("csr_projects.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.name.data},"
                           f"{form.email.data},"
                           f"{form.room.data},"
                           f"{form.table.data},"
                           f"{form.review.data},"
                           f"{form.rate.data}")

        body = f"Name of guest: {form.name.data}\nEmail: {form.email.data}\nRoom number: {form.room.data}\nTable number: {form.table.data}\nReview: {form.review.data}\nRating: {form.rate.data}\n  "
        message = MIMEMultipart()

        message["From"] = gmail
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        connection = smtplib.SMTP_SSL("smtp.gmail.com")
        connection.ehlo()
        connection.login(user=gmail, password=password)
        text = message.as_string()
        connection.sendmail(gmail, receiver, text)

        connection.quit()




        return redirect(url_for('home'))
    return render_template("feedback.html", form=form)


@app.route("/Rate staff", methods=["GET", "POST"])
def rate_staff():
    form = RateStaffForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"{form.staff_name.data},"
                           f"{form.rate.data},"
                           f"{form.review.data}")
            staff_name = form.staff_name.data
        rates = len(form.rate.data)
        rate = int(rates)
        staff_review = form.review.data
        print(rate)


        body = f"Name of staff {form.staff_name.data}\nReview: {form.review.data}\nRating: {form.rate.data}\n"
        message = MIMEMultipart()

        for name in names:
            if name == staff_name:
                staff_ratings = {
                    name: {'name': name, 'review': staff_review, 'total_ratings': rate}
                }

                staff_name = form.staff_name.data

                # Print the updated staff ratings
                with open("rating.csv", mode="a", encoding='utf-8') as csv_file:
                    csv_file.write(f'{staff_ratings[name]["name"]},'

                                   f"{staff_ratings[name]['review']},"
                                   f"{staff_ratings[name]['total_ratings']}\n"
                                   )

        return redirect(url_for('home'))
    return render_template("staffrating.html", form=form)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)