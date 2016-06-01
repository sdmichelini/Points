import jinja2
import json
import logging
import os
import webapp2

from models import points

#Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'views')),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True)

class AdminPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render({}))

app = webapp2.WSGIApplication([
	('/admin',AdminPage),
],debug = True)
