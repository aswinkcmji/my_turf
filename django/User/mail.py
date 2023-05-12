####################################################### IMPORTS REQUIRED FOR EMAIL #############################################################
from django.core.mail import EmailMultiAlternatives  ############# USED TO SEND MAIL
from django.template.loader import render_to_string  ############# USED TO RENDER HTML FILE TO STRING
from django.utils.html import strip_tags             ############# USED TO STRIP HTML  TAGS TO SEND  CONTENT AS PLAIN STRING IN CASE HTML CONTENT IIS NOT SUPPORTED

def send_email(mail_subject,content_as_plain,content_as_html,to_email):
    subject, from_email, to = mail_subject, 'myturfapp@gmail.com', to_email
    text_content = content_as_plain
    html_content = content_as_html
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()