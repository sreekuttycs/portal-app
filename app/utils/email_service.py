import requests
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_FROM_EMAIL = os.getenv("MAILGUN_FROM_EMAIL")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates", "customer")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def send_verification_email(to_email: str, username: str, token: str):
    template = env.get_template("emails/verification_email.html")
    # verification_link = f"{os.getenv('FRONTEND_URL')}/verify/{token}"
    verification_link = "http://127.0.0.1:8000/verify/{token}"

    html_content = template.render(username=username, verification_link=verification_link)

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM_EMAIL,
            "to": [to_email],
            "subject": "Verify your email",
            "html": html_content,
        },
    )
    print("Mailgun response:", response.status_code, response.text)
    return response

def send_password_reset_email(to_email: str, username: str, token: str):
    template = env.get_template("emails/password_reset_email.html")
    reset_link = f"http://127.0.0.1:8000/reset-password/{token}"

    html_content = template.render(username=username, reset_link=reset_link)

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM_EMAIL,
            "to": [to_email],
            "subject": "Reset your password",
            "html": html_content,
        },
    )
    print("Mailgun response:", response.status_code, response.text)
    return response
    