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

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render({}))

class HelpPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('help.html')
		self.response.write(template.render({}))

class PointsApi(webapp2.RequestHandler):
	def get(self):
		"""
		HTTP GET endpoints for the points api

		This returns JSON and always has a message field
		"""
		self.response.headers['Content-Type'] = 'application/json'
		term = self.request.get('term',default_value='0')
		try:
			term_int = get_term(term)
			self.response.write(json.dumps({'message':'Success', 'result':points.get_all_users_points_as_dict_for_term(term_int)}))
		except ValueError:
			self.response.set_status(400)
			self.response.write(json.dumps({'message':'Error: Invalid parameter'}))


def get_term(term_parameter):
	"""
	This method will convert a term into an integer representation of it
	"""
	if (term_parameter == 'A') or (term_parameter == 'a'):
		return 0
	elif (term_parameter == 'B') or (term_parameter == 'b'):
		return 1
	elif (term_parameter == 'C') or (term_parameter == 'c'):
		return 2
	elif (term_parameter == 'D') or (term_parameter == 'd'):
		return 3
	ret = int(term_parameter)
	return ret


app = webapp2.WSGIApplication([
	('/',MainPage),
	('/help',HelpPage),
	('/api/points',PointsApi)
],debug = True)
