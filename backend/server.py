from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop
import numpy as np
import cv2
import string
import random

import face_detector as fd

random_string = lambda x: "".join([random.choice(string.ascii_letters) for _ in range(x)])

detector = fd.FaceDetector()
output_addr = "./"

class EchoWebSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def initialize(self, detector):
        self.detector = detector

    def open(self):
        print("WebSocket opened")

    def on_message(self, data):
        img_data = np.fromstring(data, dtype=np.uint8)
        img = cv2.imdecode(img_data, 1)
        '''
        # Uncomment to see frontend sent image
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        faces = self.detector.get_faces_from_img(img)
        print(faces)
        '''
        if np.shape(faces)[0]:
            sess_id = session.get('sess_id', None)
            if sess_id is None:
                gen_sess_id = random_string(20)
                session['sess_id'] = gen_sess_id
                sess_id = gen_sess_id

            op = os.path.join(output_addr, sess_id,
                              "{}.jpg".format(random_string(30)))
            cv2.imwrite(img, op)
        '''

        for face in faces:
            bb = face.bounding_box
            self.write_message({'x': bb.x, 'y': bb.y, 'w':
                                   bb.w, 'h': bb.h})

    def on_close(self):
        print("WebSocket closed")


if __name__ == "__main__":
    app = Application([
            (r"/detect", EchoWebSocket, dict(detector=detector)),
        ])

    app.listen(5000, '0.0.0.0')
    print("{} Server started")
    IOLoop.current().start()

