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

class AdminPointsPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('points_entry.html')
		self.response.write(template.render({}))
	def post(self):
		'''
		{"title":"Test","description":"This is a
		test","points_completed":"25","points_missed":"25","mandatory":false,"user_items":[{"user":"test@example.com","weight":0.48},{"user":"bob@example.com","weight":0.4}]}
		'''
		#Check for JSON
		self.response.headers['Content-Type'] = 'application/json'
		try:
			data = json.loads(self.request.body)
			if (not 'title' in data) or (not 'description' in data) or (not 'points_completed' in data) or(not 'mandatory' in data) or (not 'user_items' in data):
				msg = {
						'message':'Not enough fields provided.'
						}
				self.response.set_status(400)
			else:
				points_item = points.PointItem(title=data['title'], description=data['description'],
						term = get_term(data['term']), points_completed =int(data['points_completed']),
						points_missed =int( data['points_missed']), mandatory= data['mandatory'])
				points.insert_points_items_with_weights(points_item, data['user_items'])
				msg = {
						'message':'Fields okay.'
						}


		except(ValueError):
			msg = {
					'message' : 'Error: Could not parse request.'
				}
			self.response.set_status(400)
		self.response.write(json.dumps(msg))

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
	('/admin',AdminPage),
	('/admin/points',AdminPointsPage)
],debug = True)
