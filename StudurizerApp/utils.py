# StudurizerApp/utils.py
import apprise
from django.conf import settings
from StudurizerApp import settings
import os
import logging

from StudurizerApp.settings import APPRISE_EMAIL_BASE

logger = logging.getLogger(__name__)

""" Use like this:
    from StudurizerApp.utils import send_email_notification
    
    send_email_notification(
    to_email="user2@example.com",
    subject="Wichtige Nachricht",
    body="Dies ist eine Nachricht an mehrere Empfänger.",
    attachment_path="/app/output/report.pdf"
    )
    """

def send_email_notification(to_email, subject, body, attachment_path=None):
    """
    Sendet eine E-Mail per Apprise an einen einzelnen Empfänger.

    :param to_email: String – Einzelne E-Mail-Adresse
    :param subject: Betreff der E-Mail
    :param body: Nachrichtentext
    :param attachment_path: Optionaler Pfad zu einer Datei (z. B. PDF)
    """
    if not to_email or not isinstance(to_email, str):
        raise ValueError("Es muss genau eine E-Mail-Adresse als String übergeben werden.")

    # Apprise-URL dynamisch bauen mit To:
    url = f"{settings.APPRISE_EMAIL_BASE}&to={to_email}"

    apobj = apprise.Apprise()
    apobj.add(url)

    kwargs = {
        'title': subject,
        'body': body,
    }

    if attachment_path:
        if not os.path.exists(attachment_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {attachment_path}")
        kwargs['attach'] = attachment_path

    logger.info(f"Sende E-Mail an {to_email} mit Betreff: '{subject}'")

    success = apobj.notify(**kwargs)

    if not success:
        logger.warning(f"E-Mail konnte nicht gesendet werden an: {to_email}")
    return success
