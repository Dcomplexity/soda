# coding:utf-8

import tornado.web
import string
import time
import datetime
import random
from model.entity import Entity
import model.get_date as getdate
import model.Users as Users
import model.orders as orders

# fake_names_old = ['lhl', 'zjh', 'lw', 'pll', 'wy', 'ygx', 'wxl', 'xzw', 'sly', 'cl', 'zsh', 'dly', 'zyf', 'yzj', 'yc', 'qxy', 'ymf', 'ssy', 'gyl', 'tys', 'ls', 'wmy']
fake_names = [u'用户1', u'用户2', u'用户3', u'用户4', u'用户5', u'用户6', u'用户7', u'用户8', u'用户9']

month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12}

stations_regular_names = [u'陆家嘴', u'静安寺', u'上海火车站', u'人民广场', u'南京东路', u'徐家汇', u'莘庄', u'陕西南路', u'中山公园',u'世纪大道']


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("login_username")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render('index.html')
        else:
            self.redirect('/function')


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        Users.create_table()
        users_name = self.get_argument('username')
        users_email = self.get_argument('useremail')
        users_drivecard = self.get_argument('drivecard')
        users_pw = self.get_argument('password')
        res = Users.checkUsers(users_name, users_email)
        if res:
            self.redirect('/')
        else:
            last_users_id = Users.Users_cu.execute('SELECT COUNT(*) FROM Users_table').fetchone()[0]
            new_users_id = last_users_id + 1
            print new_users_id
            Users.Users_cu.execute('insert into Users_table values("%d", "%s", "%s", "%s", "%s")' % (
            new_users_id, users_name, users_email, users_drivecard, users_pw))
            Users_data = Users.Users_cu.execute('SELECT * FROM Users_table').fetchall()
            print(Users_data)
            start_regular = u"人民广场"
            des_regular = u"徐家汇"
            register_fake_name = random.sample(fake_names, 3)
            Users.Users_cu.execute('INSERT INTO Users_regular_table VALUES ("%s","1","7:00-8:00","%s","%s")' %(users_name, start_regular, des_regular))
            Users.Users_cu.execute('INSERT INTO Users_regular_table VALUES ("%s","2","18:00-19:00","%s","%s")' %(users_name, des_regular, start_regular))
            Users.Users_cu.execute('INSERT INTO Rec_friends_table VALUES ("%s","1","%s","7:00-8:00","%s","%s")' %(users_name, register_fake_name[0], start_regular, des_regular))
            Users.Users_cu.execute('INSERT INTO Rec_friends_table VALUES ("%s","2","%s","18:00-19:00","%s","%s")' %(users_name, register_fake_name[1], des_regular, start_regular))
            Users.Users_cu.execute('INSERT INTO Rec_friends_table VALUES ("%s","3","%s","18:00-19:00","%s","%s")' %(users_name, register_fake_name[2], des_regular, start_regular))
            Users.Users_db.commit()
            self.set_secure_cookie("login_username", Users_data[-1][1])
            self.redirect('/function')


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        name_login = self.get_argument("username")
        email_login = self.get_argument("useremail")
        pw_login = self.get_argument("password")
        res_login = Users.checkUsers(name_login, email_login, pw_login)
        if res_login:
            self.set_secure_cookie("login_username", self.get_argument("username"))
            self.redirect("/function")
        else:
            self.redirect("/")


class FunctionHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/')
            return
        login_name = tornado.escape.xhtml_escape(self.current_user)
        self.render("function/function_index.html", function_user_name=login_name)


class QuitHandler(BaseHandler):
    def get(self):
        self.clear_cookie("login_username")
        self.redirect("/")


class OrdersHandler(BaseHandler):
    def post(self):
        order_users_name = self.get_current_user()
        order_set_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
        order_time = self.get_argument("order_time")
        order_start = self.get_argument("order_start")
        order_des = self.get_argument("order_des")
        order_people = self.get_argument("order_people")
        order_driver = self.get_argument("checkdriver")  # if this option is selected, the value is on
        order_share = self.get_argument("checkshare")
        order_users_name_id = \
        orders.orders_cu.execute("SELECT id FROM Users_table WHERE name = '%s'" % order_users_name).fetchone()[0]
        order_id = string.atoi(
            order_set_time[0:4] + order_set_time[5:7] + order_set_time[8:10] + order_set_time[11:13] + order_set_time[
                                                                                                       14:16] + order_set_time[
                                                                                                                17:19] + str(1000 + order_users_name_id))
        orders.orders_cu.execute('INSERT INTO Orders_table VALUES ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "not")' % (
        order_id, order_users_name, order_time, order_start, order_des, order_people, order_driver, order_share))
        if string.atoi(order_people) < 5 and order_share == "1":
            order_merge_name = random.sample(fake_names, 3)
            for i in range(0, len(order_merge_name)):
                order_merge_time = datetime.datetime.strptime(order_time, "%Y-%m-%d-%H:%M")
                time_change = random.randint(-10, 10)
                order_merge_time = order_merge_time + datetime.timedelta(minutes=time_change)
                order_merge_time = order_merge_time.strftime("%Y-%m-%d-%H:%M")
                order_remain_people = random.randint(1, 5-string.atoi(order_people))
                orders.orders_cu.execute('INSERT INTO Orders_merge_table VALUES ("%d","%s","%s","%s","%s","%s", "%s")' %(order_id, order_merge_name[i], order_merge_time, order_start, order_des, order_remain_people, order_users_name))
        orders.orders_db.commit();
        self.redirect("/order_unfinished")


class Order_unfinishedHandler(BaseHandler):
    def get(self):
        order_users_name = self.get_current_user()
        order_content = orders.orders_cu.execute(
            "SELECT * FROM Orders_table WHERE order_users_name = '%s'" % order_users_name).fetchall()
        time_now = time.strftime('%Y-%m-%d-%H:%M', time.localtime())
        order_content_unfinished = []
        for p in order_content:
            if p[2] > time_now:
                order_content_unfinished.append(list(p))
        print order_content_unfinished
        self.render("function/order_table_now.html", function_user_name=order_users_name,
                    order_content_unfinished=order_content_unfinished)

class Order_finishedHandler(BaseHandler):
    def get(self):
        order_users_name = self.get_current_user()
        order_content = orders.orders_cu.execute(
            "SELECT * FROM Orders_table WHERE order_users_name = '%s'" % order_users_name).fetchall()
        time_now = time.strftime('%Y-%m-%d-%H:%M', time.localtime())
        order_content_finished = []
        for p in order_content:
            if p[2] < time_now:
                order_content.finished.append(list(p))
        self.render("function/order_table_old.html", function_user_name=order_users_name,
                    order_content_finished=order_content_finished)


class Order_merge(BaseHandler):
    def get(self):
        order_users_name = self.get_current_user()
        order_id = self.get_argument("order_id")
        order_content_merge = []
        order_content = orders.orders_cu.execute("SELECT * FROM Orders_merge_table WHERE order_merge_for_name=='%s'" %order_users_name).fetchall()
        if order_id == '0':
            for p in order_content:
                order_content_merge.append(list(p))
        else:
            for p in order_content:
                if p[0] == string.atoi(order_id):
                    order_content_merge.append(list(p))
        self.render("function/order_table_merge.html", function_user_name=order_users_name, order_content_merge=order_content_merge)

class Order_merged(BaseHandler):
    def get(self):
        order_user_name = self.get_current_user()
        order_id = self.get_argument("order_id")
        order_merge_name = self.get_argument("order_merge_name")
        order_merge_people = self.get_argument("order_merge_people")
        order_origin_people = orders.orders_cu.execute("SELECT order_people FROM Orders_table WHERE id=='%d'" %string.atoi(order_id)).fetchone()
        order_merged_people = order_origin_people[0] + string.atoi(order_merge_people)
        orders.orders_cu.execute("UPDATE Orders_table SET order_people='%d', order_status='%s' WHERE id=='%d'" %(order_merged_people, order_merge_name, string.atoi(order_id)))
        orders.orders_cu.execute("DELETE FROM Orders_merge_table WHERE order_id=='%d'" %string.atoi(order_id))
        orders.orders_db.commit()
        self.redirect('/order_unfinished')

class Order_delete(BaseHandler):
    def get(self):
        order_id = self.get_argument("order_id")
        orders.orders_cu.execute("DELETE FROM Orders_table WHERE id=='%d'" %string.atoi(order_id))
        orders.orders_cu.execute("DELETE FROM Orders_merge_table WHERE order_id=='%d'" %string.atoi(order_id))
        orders.orders_db.commit()

class Changeregular1(BaseHandler):
    def post(self):
        user_name = self.get_current_user()
        regular_time = self.get_argument("regular_time")
        regular_start = self.get_argument("regular_start")
        regular_des = self.get_argument("regular_des")
        orders.orders_cu.execute("UPDATE Users_regular_table SET regular_time='%s', start='%s', des='%s' WHERE regular_id='1' AND users_name='%s'"
                                 %(regular_time, regular_start, regular_des, user_name))
        orders.orders_db.commit()
        self.redirect("/friend_recommendation")
        print(regular_time)
        print(regular_start)
        print(regular_des)

class Changeregular2(BaseHandler):
    def post(self):
        user_name = self.get_current_user()
        regular_time = self.get_argument("regular_time")
        regular_start = self.get_argument("regular_start")
        regular_des = self.get_argument("regular_des")
        orders.orders_cu.execute("UPDATE Users_regular_table SET regular_time='%s', start='%s', des='%s' WHERE regular_id='2' AND users_name='%s'"
                                 %(regular_time, regular_start, regular_des, user_name))
        self.redirect("/friend_recommendation")
        print(regular_time)
        print(regular_start)
        print(regular_des)

class FriendRecommendationHandler(BaseHandler):
    def get(self):
        user_name = self.get_current_user()
        regular_content = orders.orders_cu.execute("SELECT * FROM Users_regular_table WHERE users_name='%s'" %user_name).fetchall()
        recommendation_name = random.sample(fake_names, 3)
        orders.orders_cu.execute("UPDATE Rec_friends_table SET rec_name='%s',time='%s',start='%s',des='%s' WHERE rec_id='1' AND user_name='%s'"
                                     %(recommendation_name[0],regular_content[0][2],regular_content[0][3],regular_content[0][4], user_name))
        orders.orders_cu.execute("UPDATE Rec_friends_table SET rec_name='%s',time='%s',start='%s',des='%s' WHERE rec_id='2' AND user_name='%s'"
                                     %(recommendation_name[1],regular_content[1][2],regular_content[1][3],regular_content[1][4], user_name))
        orders.orders_cu.execute("UPDATE Rec_friends_table SET rec_name='%s',time='%s',start='%s',des='%s' WHERE rec_id='3' AND user_name='%s'"
                                     %(recommendation_name[2],regular_content[1][2],regular_content[1][3],regular_content[1][4], user_name))
        orders.orders_db.commit()
        rec_friends = orders.orders_cu.execute("SELECT * FROM Rec_friends_table WHERE user_name='%s'" %user_name).fetchall()
        self.render("function/friends_recommendation.html", function_user_name=user_name, regular_content_show = regular_content,
                    rec_friends=rec_friends)

class FriendMangerHandler(BaseHandler):
    def get(self):
        date_time = time.strftime('%Y-%m-%d', time.localtime())
        date_now = datetime.datetime.strptime(date_time, "%Y-%m-%d")
        date_change = random.randint(1, 4)
        new_order_date = date_now + datetime.timedelta(days=date_change)
        new_time = getdate.get_date()+"-7:30"
        print new_time
        user_name = self.get_current_user()
        self.render("function/friends_manage.html", function_user_name=user_name, new_time=new_time)

class OrderGrouponHandler(BaseHandler):
    def get(self):
        new_time = getdate.get_date()+"-19:00-20:00"
        user_name = self.get_current_user()
        self.render("function/order_groupon.html", function_user_name=user_name, new_time=new_time)

class AddGrouponOrderHandler(BaseHandler):
    def post(self):
        order_users_name = self.get_current_user()
        new_time = self.get_argument("new_time")
        print new_time
        stations = self.get_argument("stations")
	print "1"
	print "2"
        start_des = stations.split("->")
        order_start = start_des[0]
        order_des = start_des[1]
        order_set_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
        order_users_name_id = \
        orders.orders_cu.execute("SELECT id FROM Users_table WHERE name = '%s'" % order_users_name).fetchone()[0]
        order_id = string.atoi(
            order_set_time[0:4] + order_set_time[5:7] + order_set_time[8:10] + order_set_time[11:13] + order_set_time[
                                                                                                       14:16] + order_set_time[
                                                                                                                17:19] + str(1000 + order_users_name_id))
        orders.orders_cu.execute('INSERT INTO Orders_table VALUES ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "not")' % (
        order_id, order_users_name, new_time, order_start, order_des, "1", "1", "0"))
        orders.orders_db.commit()

class AttendFriendsHandler(BaseHandler):
    def post(self):
        order_users_name = self.get_current_user()
        friends_name = self.get_argument("friends_name")
        information = self.get_argument("information")
        time_stations = information.split("--")
        start_des = time_stations[1].split("->")
        new_time = time_stations[0]
        order_start = start_des[0]
        order_des = start_des[1]
        order_set_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
        order_users_name_id = \
        orders.orders_cu.execute("SELECT id FROM Users_table WHERE name = '%s'" % order_users_name).fetchone()[0]
        order_id = string.atoi(
            order_set_time[0:4] + order_set_time[5:7] + order_set_time[8:10] + order_set_time[11:13] + order_set_time[
                                                                                                       14:16] + order_set_time[
                                                                                                                17:19] + str(1000 + order_users_name_id))
        orders.orders_cu.execute('INSERT INTO Orders_table VALUES ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
        order_id, order_users_name, new_time, order_start, order_des, "2", "1", "0", friends_name))
        orders.orders_db.commit()


