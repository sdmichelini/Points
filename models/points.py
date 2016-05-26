from google.appengine.ext import ndb
from time import mktime

import datetime
import json
import logging

TERMS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'All Year'}

class DateJsonEncoder(json.JSONEncoder):
	def default(self,obj):
		if(isinstance(obj, datetime.datetime)):
			return int(mktime(obj.timetuple()))
		return json.JSONEncoder.default(self,obj)


class PointItem(ndb.Model):
	#Title of the Point Item, ie: House Meeting
	title = ndb.StringProperty(required=True)
	#Description of the Points Item
	description = ndb.StringProperty()
	#Which Term Did it Occur?
	term = ndb.IntegerProperty(choices=TERMS.keys(), default=4)
	#When
	date = ndb.DateTimeProperty(auto_now_add = True)
	#Points awarded for completing the event
	points_completed = ndb.IntegerProperty(required=True)
	#Points awarded for missing the event
	points_missed = ndb.IntegerProperty(required=True)
	#Is the event madatory?
	mandatory = ndb.BooleanProperty(default=False)
	

class UserPointItem(ndb.Model):
	#Email of User
	user_email = ndb.StringProperty(required=True)
	#PointItem that they are recieving/losing points for
	point_item = ndb.StructuredProperty(PointItem, required = True)
	#Did they complete it
	completed = ndb.BooleanProperty(required = True)
	'''
	Get's the points for a specified user. It will query the UserPointItem to find all the points for a user
	
	Returns an integer with the points
	'''
	@classmethod
	def get_points_for_user_in_term(self, email,term):
		results = self.query().filter(self.user_email == email,self.point_item.term==term).fetch()
		if len(results) == 0:
			return 0
		else:
			sum_points = 0
			for item in results:
				if item.completed:
					sum_points += item.point_item.points_completed
				else:
					sum_points -= item.point_item.points_missed
			return sum_points
	'''
	Get's the points for all users in a specific term. It will query the UserPointItem to find all the points for a user

	Returns a dictionary with the key being the users email and the value being the points
	'''
	@classmethod
	def get_points_for_all_users_in_term(self, term):
		results = self.query().filter(self.point_item.term == term).fetch()
		ret = {}
		for item in results:
			if item.completed:
				ret[item.user_email] = ret.get(item.user_email, 0) + item.point_item.points_completed
			else:
				ret[item.user_email] = ret.get(item.user_email, 0) - item.point_item.points_missed
		return ret
