import csv
import os
import smtplib
import json
import ssl
import logging

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.colors import white

from PyPDF2 import PdfReader, PdfWriter


# Set the log level to info and specify the format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s',
)
log = logging.getLogger(__name__)


# Paths for the resources
NAMELIST_CSV = os.path.abspath("data/raw_data.csv")
CERT_TEMPLATE = os.path.abspath("templates/certificate_template.pdf")
PARTICIPANT_TEMPLATE = os.path.abspath("templates/participant_name_template.pdf")
SETTINGS_FILE = os.path.abspath("config/settings.json")


def load_settings():
    """Load settings from the JSON configuration file."""
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except FileNotFoundError as e:
        log.error(f"Settings file not found: {e}")
        return {}
    except json.JSONDecodeError as e:
        log.error(f"Error decoding JSON: {e}")
        return {}


settings = load_settings()
gmail_user = settings.get('gmail_user', '')
gmail_password = settings.get('gmail_password', '')


def create_certificate_pdf(name, cert_template=CERT_TEMPLATE, participant_template=PARTICIPANT_TEMPLATE):
    """
    Create a PDF certificate for the participant and return the output path.
    Combines a certificate template with the participant's name.
    """
    try:
        # Create the participant name PDF overlay
        participant_pdf_path = f"output/{name.strip().replace(' ', '_').lower()}_overlay.pdf"
        canvas = Canvas(participant_pdf_path, pagesize=landscape(LETTER))
        canvas.setFont("Helvetica-Bold", 40)
        canvas.setFillColor(white)
        canvas.drawString(4.1 * inch, 4.60 * inch, name)
        canvas.save()

        # Combine the overlay with the certificate template
        output_file_path = f"output/{name.strip().replace(' ', '_').lower()}.pdf"
        with open(cert_template, "rb") as cert_file, open(participant_pdf_path, "rb") as participant_file:
            cert_reader = PdfReader(cert_file)
            participant_reader = PdfReader(participant_file)

            output_pdf = PdfWriter()
            input_page = cert_reader.pages[0]
            input_page.merge_page(participant_reader.pages[0])
            output_pdf.add_page(input_page)

            with open(output_file_path, "wb") as outputStream:
                output_pdf.write(outputStream)

        return output_file_path

    except Exception as e:
        log.error(f"Error creating certificate for {name}: {e}")
        return None


def form_email_message(name, to_email, subject, body, participant_cert):
    """Create an email message with an attachment."""
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg['From'] = gmail_user
    email_msg['To'] = to_email
    email_msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF certificate
    try:
        with open(participant_cert, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(participant_cert)}",
            )
            email_msg.attach(part)
    except FileNotFoundError as e:
        log.error(f"Attachment not found: {e}")
    
    return email_msg.as_string()


def send_email(name, to_email, participant_cert):
    """Send the email with the attached certificate."""
    subject = "Your Certificate of Participation"
    body = f"""
    Hi {name},

    Thank you for attending the tennis event and for your invaluable contribution to our victory in the Singapore Cup!

    We hope you had an amazing time and enjoyed the experience. We look forward to welcoming you again next year.

    Please find your Certificate of Participation attached.

    Warm regards,
    """
    email_msg = form_email_message(name, to_email, subject, body, participant_cert)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, email_msg)
            log.info(f"Email sent to {to_email}")
    except smtplib.SMTPException as e:
        log.error(f"Failed to send email to {to_email}: {e}")


def process_certificates():
    """Main process to generate certificates and send emails."""
    try:
        with open(NAMELIST_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                participant_name = row['name']
                participant_email = row['email']
                log.info(f"Creating certificate for {participant_name}")

                participant_cert = create_certificate_pdf(participant_name)
                if participant_cert:
                    send_email(participant_name, participant_email, participant_cert)

        log.info("All certificates created and emails sent.")
    except FileNotFoundError as e:
        log.error(f"CSV file not found: {e}")
    except csv.Error as e:
        log.error(f"Error reading CSV file: {e}")


if __name__ == "__main__":
    process_certificates()
