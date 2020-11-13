from django.template.loader import render_to_string

from management.utils import send_html_email


def subscribe_success(addr, context):
    subject = 'subscribe success'
    html = render_to_string('html_template.html', context=context)
    send_html_email([addr], subject, html)


def check_warn(p: int, pl: list) -> int:
    pl = list(map(lambda x: x - p, pl))
    cnt = 0
    flag = pl[0]
    if flag == 0:
        cnt = 1
    for i in range(len(pl) - 1):
        if (pl[i + 1] == 0 and flag != 0) or (pl[i] * pl[i + 1] < 0):
            cnt += 1
        flag = pl[i + 1]
    return cnt
