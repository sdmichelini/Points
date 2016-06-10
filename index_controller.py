import base64
import jinja2
import json
import logging
import os
import webapp2

from flags import flags

from models import points
from models import users

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


class AllUsers(webapp2.RequestHandler):
	def get(self):
		"""HTTP GET endpoit for users api

		This returns JSON and always has a message field
		"""
		self.response.headers['Content-Type'] = 'application/json'
		msg = {'message': 'Success', 'result': users.get_all_users()}
		self.response.write(json.dumps(msg))

class UserDetails(webapp2.RequestHandler):
	def get(self, user_id):
		"""HTTP Get Endpoint for Specific User

		"""

		self.response.headers['Content-Type'] = 'application/json'
		success = False
		try:
			email = base64.b64decode(user_id)
			results = points.UserPointItem.query(points.UserPointItem.user_email == email).fetch()
			success = True
		except:
			logging.exception('')
			self.response.set_status(400)
			self.response.write(json.dumps({'msg': 'Error Decoding User-Id'}))
		if success:
			if len(results) < 1:
				self.response.set_status(404)
				self.response.write(json.dumps({'msg':'Error: User not found.'}))
			else:
				self.response.write(json.dumps({'msg':'Success', 'results' : json.dumps([p.to_dict() for p in results], cls = points.DateJsonEncoder)}))
				self.response.write(json.dumps({'msg':'User ID', 'id': email}))


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

def handle_404(request, response, exception):
	logging.exception(exception)
        #response.write('Oops! I could swear this page was here!')
	template = JINJA_ENVIRONMENT.get_template('not_found.html')
	response.write(template.render({}))
	response.set_status(404)

app = webapp2.WSGIApplication([
	('/',MainPage),
	('/help',HelpPage),
	('/api/points',PointsApi),
	('/users', AllUsers),
	(r'/users/([a-zA-Z0-9=]*)', UserDetails)
],debug = True)

app.error_handlers[404] = handle_404
