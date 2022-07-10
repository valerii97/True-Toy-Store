from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_order_email(email, order_data_list):
    plaintext = get_template('shop/email.txt')
    htmltext = get_template('shop/email.html')

    data = {
        'order_data_list': order_data_list,
    }

    subject, from_email, to = 'Order is completed', 'tts@gmail.com', email

    text_content = plaintext.render(data)
    html_content = htmltext.render(data)

    msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to])

    msg.attach_alternative(html_content, "text/html")

    msg.send()