from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(user, verification_url):
    subject = f'Verify your email for {settings.SITE_NAME}'
    
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL
    }
    
    # HTML içeriği
    html_content = render_to_string('accounts/emails/verify_email.html', context)
    # Text içeriği
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject,
        text_content,
        f'{settings.SITE_NAME} <{settings.EMAIL_HOST_USER}>',
        [user.email]
    )
    
    email.attach_alternative(html_content, "text/html")
    email.send()