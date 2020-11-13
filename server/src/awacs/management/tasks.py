import dramatiq
import logging

from management.utils import send_html_email

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=0)
def send_html_email_task(to_list, subject, html):
    try:
        send_html_email(to_list, subject, html)
    except Exception as e:
        logger.error(e)
