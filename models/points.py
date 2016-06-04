from google.appengine.ext import ndb
from time import mktime

import datetime
import json
import logging

TERMS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'All Year'}

#Cache for all users points item
POINTS_CACHE = {}

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
	#Weight
	weight = ndb.FloatProperty(default=1.0)
	@classmethod
	def get_points_for_user_in_term(self, email,term):
		'''
		Get's the points for a specified user. It will query the UserPointItem to find all the points for a user

		Returns an integer with the points
		'''
		results = self.query().filter(self.user_email == email,self.point_item.term==term).fetch()
		if len(results) == 0:
			return 0
		else:
			sum_points = 0
			for item in results:
				if item.completed:
					sum_points += item.weight * item.point_item.points_completed
				else:
					sum_points -= item.point_item.points_missed
			return sum_points
	'''
	Get's the points for all users in a specific term. It will query the UserPointItem to find all the points for a user

	Returns a dictionary with the key being the users email and the value being the points
	'''
	@classmethod
	def get_points_for_all_users_in_term(self, term):
		results = self.query().filter(self.point_item.term == int(term)).fetch()
		ret = {}
		for item in results:
			if item.completed:
				ret[item.user_email] = ret.get(item.user_email, 0) + item.point_item.points_completed
			else:
				ret[item.user_email] = ret.get(item.user_email, 0) - item.point_item.points_missed
		return ret

'''
Create's a new points item and adds users to it.

Args:
	points_item: An instance of a UserPointItem class. Not in NDB yet!
	completed: a list of emails of users who have completed points_item
	missed: a list of emails of users who have not completed points_item

Returns:
	none
'''
def insert_points_item_with_users(points_item, completed, missed):
	flush_cache()
	#Put the points item in ndb
	points_item.put()
	#Create a list for put_multi
	point_items = list()
	#Now iterate through completed and not completed
	for _user_email in completed:
		point_items.append(UserPointItem(user_email = _user_email, point_item=points_item, completed=True))
	for _user_email in missed:
		point_items.append(UserPointItem(user_email = _user_email, point_item=points_item, completed=False))
	ndb.put_multi(point_items)


def insert_points_items_with_weights(points_item, completed_dict):
	"""
	Insert users points item with a weight.

	Args:
		points_item: NDB Model for the Overall Points Item
		completed_dict: Dictionary with the email as keys and actual email as values
	"""
	flush_cache()
	points_item.put()
	point_items = list()
	for _user_email in completed_dict:
		point_items.append(UserPointItem(user_email = _user_email['user'], point_item=points_item,
						completed = _user_email['completed'], weight = _user_email['weight']))
	ndb.put_multi(point_items)
		

def get_all_users_points_as_dict_for_term(term):
	"""
	Get's all user's total points for a given term. It uses caching to reduce database queries

	Args:

		term: Integer representing the term that is requested

	Returns:

		A dictionary with the keys being the users emails and the values being their points sum.
	"""
	global POINTS_CACHE
	if term in POINTS_CACHE:#The cache is populated
		return POINTS_CACHE.get(term)
	else:#The cache is not populated
		POINTS_CACHE = get_points_cache()
		return POINTS_CACHE.get(term)

def get_user_points_for_term(user, term):
	"""
	Get's a users points for a given term.

	Args:
		user: Email of User
		term: Integer representing the term requested

	Returns:
		Integer with the points for a user in the current term
	"""
	all_users = get_all_users_points_as_dict_for_term(term)
	ret = all_users.get(user)
	if ret is None:
		return 0
	else:
		return ret

def get_points_cache():
	"""
	Get's a copy of the Python dictionary to populate the points cache. Note
	this method does not actually assign the value to POINTS_CACHE

	Args:
		None
	Returns:
		Python dictionary of all the terms points
	"""
	logging.error('Points database hit!')
	global TERMS
	ret_dict = {}
	for key in TERMS:
		ret_dict[key] = UserPointItem.get_points_for_all_users_in_term(key)
	return ret_dict
def flush_cache():
	global POINTS_CACHE
	POINTS_CACHE.clear()
