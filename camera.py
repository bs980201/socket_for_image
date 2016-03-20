import cv2
import time
# import swiftclient
import redis

def upload_to_swift(swift, contain_name, file_name):
    #Upload the object
    with open(file_name, 'rb') as f:
        file_data = f.read()
    swift.put_object(contain_name, file_name, file_data)
    return swift

def get_in_swift():
    username = 'hackthon3'
    password = 'quahbixu'
    tenant_name = 'hackthon3'
    auth_url = 'http://172.17.18.3:5000/v2.0'

    swift = swiftclient.client.Connection(auth_version='2',
                                          user=username,
                                          key=password,
                                          tenant_name=tenant_name,
                                          authurl=auth_url)
    return swift

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        self.redis_save(jpeg)
        return jpeg.tobytes()

    def save_image(self):
        success,image = self.video.read()
        fileName =  "images/" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        # print fileName
        cv2.imwrite(fileName, image)

        print type(image)
        s = get_in_swift()
        s = upload_to_swift(s, 'clyde_contain02', fileName)

    def redis_save(self, jpegImage):
        redisImageName =  'imagedata'
        r = redis.StrictRedis(host='localhost')
        r.set(redisImageName, jpegImage)
