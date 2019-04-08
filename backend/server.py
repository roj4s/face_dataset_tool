from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer, ssl
import numpy as np
import cv2
import string
import random
import os

'''
#Face detection is performed on users' browser now
import face_detector as fd
detector = fd.FaceDetector()
'''

random_string = lambda x: "".join([random.choice(string.ascii_letters) for _ in range(x)])
output_addr = "/tmp"

class WS(WebSocketHandler):

    def check_origin(self, origin):
        return True

    '''
    #Face detection is performed on users' browser now
    def initialize(self, detector):
        self.detector = detector
    '''

    def open(self):
        self.sess_id = random_string(30)
        self.user_folder = os.path.join(output_addr, self.sess_id)
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
        print("Session opened for id: {}".format(self.sess_id))
        self.images_saved = 0

    def on_message(self, data):
        img_data = np.fromstring(data, dtype=np.uint8)
        img = cv2.imdecode(img_data, 1)
        '''
        # Uncomment to see frontend sent image
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        '''
        #Face detection is performed on users' browser now
        faces = self.detector.get_faces_from_img(img)
        print("Foung {} faces".format(np.shape(faces)[0]))
        if np.shape(faces)[0]:
            op = os.path.join(self.user_folder,
                              "{}.jpg".format(random_string(30)))
            cv2.imwrite(op, img)

        for face in faces:
            bb = face.bounding_box
            self.write_message({'x': bb.x, 'y': bb.y, 'w':
                                   bb.w, 'h': bb.h})
        '''
        op = os.path.join(self.user_folder,
                              "{}.jpg".format(random_string(30)))
        cv2.imwrite(op, img)
        self.images_saved += 1
        self.write_message("{} Images saved so far ...".format(self.images_saved))

    def on_close(self):
        print("WebSocket closed")


if __name__ == "__main__":
    app = Application([
            #Face detection is performed on users' browser now
            #(r"/detect", WS, dict(detector=detector)),
            (r"/capture", WS),
        ])

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("/etc/letsencrypt/live/feis.in/fullchain.pem",
                            "/etc/letsencrypt/live/feis.in/privkey.pem")
    server = HTTPServer(app, ssl_options=ssl_ctx)
    server.bind('5000', '0.0.0.0')
    server.start(0)
    print("{} Server started")
    IOLoop.current().start()

