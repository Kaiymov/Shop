from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

from iqos import settings



def activate_account(email, code):
    send_mail(
        'Activate this code',
        f'Ваш код активации - {code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def checkout_order_msg(email, f_name, order, items, shipping_address):
    subject = f'Ваш заказ в пути, {f_name}'
    html_content = render_to_string(
        'email_msg/checkout_msg.html',
        {
            'items': items,
            'order': order,
            'name': f_name,
            'shipping_address': shipping_address

         })
    text_content = strip_tags(html_content)


    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()