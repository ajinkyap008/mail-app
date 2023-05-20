from flask import Flask, render_template, make_response
from flask import request
import base64
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import traceback

app = Flask(__name__)

def send_mail(reciever_mail):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'xxx'#SendInBlue's API Key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "xxx" #mail subject
    sender = {"name":"xxx","email":"xxx"} #sender details
    html_content = "<html><body>xxx</body></html>" #html content for mail body
    to = [{"email": reciever_mail}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return "Success", 200
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return "Bad Request. Exception when calling SMTPApi->send_transac_email: %s\n" % e, 400

def encode_auth_base_string(input_string):
    byte_msg = input_string.encode('utf-8')
    base64_val = base64.b64encode(byte_msg)
    return "Basic " + base64_val.decode('utf-8')

@app.route("/authenticate")
def home_two():
    try:
        if 'Authorization' in request.headers and 'Reciever' in request.headers:
            auth_header = request.headers['Authorization']
            reciever_header = request.headers['Reciever']
            if auth_header == encode_auth_base_string("xxx:xxx") and reciever_header is not None:#basic authentication for API, requires username password
                return "Success", 200
            else:
                return "Authentication Failed", 401
        else:
            return "Authentication Failed", 401
    except Exception as e:
        traceback.print_exc()
        return str(e), 400

@app.route("/test")
def home_three():
    return "Success", 200

@app.route("/send-mail")
def home():
    try:
        if 'Authorization' in request.headers and 'Reciever' in request.headers:
            auth_header = request.headers['Authorization']
            reciever_header = request.headers['Reciever']
            if auth_header == encode_auth_base_string("xxx:xxx") and reciever_header is not None:
                return send_mail(reciever_header)
            else:
                return "Bad Authentication", 401
        else:
            return "Bad Authentication", 401
    except Exception as e:
        return str(e), 400
