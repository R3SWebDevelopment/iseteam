from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import Context
from django.template.loader import get_template
from django.utils.html import strip_tags


class Email(object):
	def __init__(self, to, subject, context_render, template):
		self.to = to
		self.subject = subject
		self.context_render = context_render
		self.template = template


	def send(self):
		dic_render = Context(self.context_render)
		html_content = get_template(self.template).render(dic_render)
		text_content = strip_tags(html_content)
		new_mail = EmailMultiAlternatives(self.subject, text_content, '', self.to)
		new_mail.attach_alternative(html_content, 'text/html')
		new_mail.send()


