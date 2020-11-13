import logging
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from django.conf import settings

logger = logging.getLogger(__name__)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_html_email(to_list, subject, html):
    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = _format_addr('每日comment <%s>' % settings.EMAIL_FROM_ADDR)
    msg['To'] = ';'.join([_format_addr('你好! <%s>' % addr) for addr in to_list])
    msg['Subject'] = Header(subject, 'utf-8').encode()

    try:
        server = smtplib.SMTP(settings.EMAIL_SMTP_SERVER, settings.EMAIL_PORT)
        server.starttls()
        server.set_debuglevel(1)
        server.login(settings.EMAIL_FROM_ADDR, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_FROM_ADDR, to_list, msg.as_string())
        server.quit()
    except Exception as e:
        logger.error(e)
