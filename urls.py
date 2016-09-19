#coding:utf-8

from handlers.index import MainHandler
from handlers.index import RegisterHandler
from handlers.index import LoginHandler
from handlers.index import FunctionHandler
from handlers.index import QuitHandler
from handlers.index import OrdersHandler
from handlers.index import Order_unfinishedHandler
from handlers.index import Order_merge
from handlers.index import Order_merged
from handlers.index import Order_delete
from handlers.index import Order_finishedHandler
from handlers.index import FriendRecommendationHandler
from handlers.index import Changeregular1
from handlers.index import Changeregular2
from handlers.index import FriendMangerHandler
from handlers.index import OrderGrouponHandler
from handlers.index import AddGrouponOrderHandler
from handlers.index import AttendFriendsHandler

urls = [
	(r'/', MainHandler),
	(r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/function', FunctionHandler),
    (r'/quit', QuitHandler),
    (r'/order', OrdersHandler),
    (r'/order_unfinished', Order_unfinishedHandler),
    (r'/order_merge', Order_merge),
    (r'/order_merged', Order_merged),
    (r'/order_delete', Order_delete),
    (r'/order_finished', Order_finishedHandler),
    (r'/friend_recommendation', FriendRecommendationHandler),
    (r'/change_regular_1', Changeregular1),
    (r'/change_regular_2', Changeregular2),
    (r'/friend_manage', FriendMangerHandler),
    (r'/order_groupon', OrderGrouponHandler),
    (r'/add_groupon_order', AddGrouponOrderHandler),
    (r'/attend_friends', AttendFriendsHandler),
]