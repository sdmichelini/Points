import jinja2
import logging
import os
import webapp2

#Jinja
JINJA_ENVIRONMENT = jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'views')),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render({}))

class HelpPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('help.html')
		self.response.write(template.render({}))

app = webapp2.WSGIApplication([
	('/',MainPage),
	('/help',HelpPage)
],debug = True)
