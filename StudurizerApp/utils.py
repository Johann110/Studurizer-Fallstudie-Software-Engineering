# StudurizerApp/utils.py
import apprise
from django.conf import settings
from StudurizerApp import settings
import os
import logging

logger = logging.getLogger(__name__)

""" Use like this:
    from StudurizerApp.utils import send_email_notification
    
    send_email_notification(
    to_emails=["user1@example.com", "user2@example.com"],
    subject="Wichtige Nachricht",
    body="Dies ist eine Nachricht an mehrere Empfänger.",
    attachment_path="/app/output/report.pdf"
    )
    """
def send_email_notification(to_emails, subject, body, attachment_path=None):
    """
    Sendet eine E-Mail per Apprise, bei der alle Empfänger als BCC gesendet werden.

    :param to_emails: Liste oder String – Empfänger
    :param subject: Betreff der E-Mail
    :param body: Nachrichtentext
    :param attachment_path: Optionaler Pfad zu einer Datei (z. B. PDF)
    """

    if not to_emails:
        raise ValueError("Empfängeradresse(n) dürfen nicht leer sein.")

    # Kommagetrennter String aus Liste oder einzelner Adresse
    if isinstance(to_emails, list):
        bcc = ','.join(to_emails)
    else:
        bcc = to_emails

    # Apprise-URL dynamisch bauen mit BCC
    url = f"{settings.APPRISE_EMAIL_BASE}/?bcc={bcc}"

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

    logger.info(f"Sende E-Mail (BCC) an {bcc} mit Betreff: '{subject}'")

    success = apobj.notify(**kwargs)

    if not success:
        logger.warning(f"E-Mail konnte nicht gesendet werden an: {bcc}")
    return success
