import sys
sys.path.insert(1,'/usr/local/google_appengine')
sys.path.insert(1,'/usr/local/google_appengine/lib/yaml/lib')

import time
import unittest

from models import points
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class PointsTestCase(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		ndb.get_context().clear_cache()

	def tearDown(self):
		points.flush_cache()
		self.testbed.deactivate()

	def testGetUserPointsTerm(self):
		points_count = points.UserPointItem.get_points_for_user_in_term('test@example.com', 2)
		self.assertEqual(0, points_count)
		point_item2 = points.PointItem(title='My Points Item',
					points_completed=5,
					points_missed=5,
					term=2)
		point_item2.put()
		user_point_item = points.UserPointItem(user_email='test@example.com',
							point_item = point_item2,
							completed=True)
		user_point_item.put()
		points_count = points.UserPointItem.get_points_for_user_in_term('test@example.com',2)
		self.assertEqual(5, points_count)
		self.assertEqual(0, points.UserPointItem.get_points_for_user_in_term('test@example.com',3))
		self.assertEqual(0, points.UserPointItem.get_points_for_user_in_term('test@gmail.com',2))

		user_point_item2 = points.UserPointItem(user_email='joe@example.com',
							point_item = point_item2,
							completed=False)
		user_point_item2.put()
		self.assertEqual(-5, points.UserPointItem.get_points_for_user_in_term('joe@example.com',2))

	def testGetAllUsersPointsTerm(self):
		points_dict = points.UserPointItem.get_points_for_all_users_in_term(2)
		self.assertEqual({}, points_dict)
		point_item2 = points.PointItem(title='My Points Item',
					points_completed=5,
					points_missed=5,
					term=2)
		point_item2.put()
		user_point_item = points.UserPointItem(user_email='test@example.com',
							point_item = point_item2,
							completed=True)
		user_point_item.put()
		points_dict = points.UserPointItem.get_points_for_all_users_in_term(2)
		self.assertEqual(1, len(points_dict))
		self.assertEqual(5, points_dict.get('test@example.com'))
		points_dict = points.UserPointItem.get_points_for_all_users_in_term(1)
		self.assertEqual({}, points_dict)

	def testInsertPointsItem(self):
		completed = ['test@example.com', 'test2@example.com']
		missed = ['joe@example.com']
		point_item2 = points.PointItem(title='My Points Item',
					points_completed=5,
					points_missed=5,
					term=2)
		points.insert_points_item_with_users(point_item2, completed, missed)
		self.assertEqual(5, points.UserPointItem.get_points_for_user_in_term('test@example.com',2))
		self.assertEqual(5, points.UserPointItem.get_points_for_user_in_term('test2@example.com',2))
		self.assertEqual(-5, points.UserPointItem.get_points_for_user_in_term('joe@example.com',2))

	def testGetUsersWithCache(self):
		points_dict = points.get_all_users_points_as_dict_for_term(2)
		self.assertEqual({}, points_dict)
		point_item3 = points.PointItem(title='My Points Item 2',
					points_completed=5,
					points_missed=5,
					term=2)
		point_item3.put()
		points.insert_points_item_with_users(point_item3, ['joe@example.com'], [])
		points_dict = points.get_all_users_points_as_dict_for_term(2)
		self.assertEqual(1, len(points_dict))
		self.assertEqual(5, points_dict.get('joe@example.com'))
		points_dict = points.get_all_users_points_as_dict_for_term(1)
		self.assertEqual({}, points_dict)



if __name__ == '__main__':
	unittest.main()
