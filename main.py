from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)

url = "https://api.npoint.io/18465676e4e60c2660ab"
data = requests.get(url).json()

MY_EMAIL = "thinhvuduc1210@gmail.com"
MY_PASSWORD = "blrcrdhiunfkfwwp"


@app.route("/")
def home():
    return render_template("index.html", posts=data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_email(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=email_message
        )


@app.route("/post/<index>")
def show_post(index):
    requested_post = None
    for post in data:
        if post["id"] == int(index):
            requested_post = post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)