import os
import pymongo
# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, removeslash
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine
import tornado.web
import uuid
# Other libraries
import json
from bson import ObjectId


salt = uuid.uuid4().hex
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["inout"]
db = mydb["customers"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def save_image(file):
    input_file = open("uploads/" + file['filename'], 'wb')
    input_file.write(file['body'])
    input_file.close()

class DetailsHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    @removeslash
    @coroutine
    def post(self):
        file = self.request.files['file'][0]
        self.request.headers['Content-Type'] = 'multipart/form-data'
        # self.request.connection.set_max_body_size(100000000000000000000)
        save_image(file)
        response = {}
        response['Name'] = 'Test'
        response['Facebook'] = 'fb.com'
        self.write(response)


class LoginHandler(RequestHandler):
    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        username = self.get_argument('username')
        file = self.request.files['file'][0]
        self.request.headers['Content-Type'] = 'multipart/form-data'
        # self.request.connection.set_max_body_size(100000000000000000000)
        save_image(file)
        data = db.userDetails.find({'uname': username})
        finalData = None
        for i in data:
            finalData = i
        if (finalData['password'] == password):
            self.write({"Response": True})
        else:
            self.write({"Response": False})


class SignUpHandler(RequestHandler):
    @coroutine
    @removeslash
    def post(self):
        username = self.get_argument('username')
        file = self.request.files['file'][0]
        self.request.headers['Content-Type'] = 'multipart/form-data'
        # self.request.connection.set_max_body_size(100000000000000000000)
        save_image(file)
        finalData = None
        data = db.userDetails.find({'uname': username})
        for i in data:
            finalData = i

        if (finalData is None):
            user_path = "uploads/data/"+file['filename']
            if not os.path.exists("uploads/data/"+ user_path):
                os.makedirs(user_path)
            db.userDetails.insert({"uname": username, "photo_path": user_path})
            self.write({"Response": True})
        else:
            self.write({'Response': False})

application = tornado.web.Application([
    (r'/signUp', SignUpHandler),
    (r'/login', LoginHandler),
    (r'/uploadDetails', DetailsHandler)
], db=db, debug=True)


def my_callback(result, error):
    print('result %s' % repr(result))
    IOLoop.instance().stop()


# main init
if __name__ == "__main__":
    application = HTTPServer(application)
    application.listen(6969)
    tornado.ioloop.IOLoop.instance().start()
