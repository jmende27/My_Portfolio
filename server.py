from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage



app = Flask(__name__)
#print(__name__)


@app.route("/")
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', mode='a') as database:
        email= data["email"]
        subject = data["subject"]
        message= data["message"]
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])


def send_email(data):
    email_to = 'judithmendez1995@gmail.com'

    #Creating email using email library
    email = EmailMessage()
    email['from'] = 'Portfolio Contact Form'
    email['to'] = email_to
    email['subject'] = 'Incoming message from website!'
    email.set_content('Someone is reaching out to you through your website contact form!')

    #Creating SMTP server using smtplib
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('gmail', 'password')
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            send_email(data)
            return redirect('/thankyou.html')
        except:
            return redirect('/contactError.html')
    else:
        return redirect('/contactError.html')
