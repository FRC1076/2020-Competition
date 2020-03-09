import socket
import time

class lights:
    def __init__(self, local_ip='10.10.76.2', ip_address='10.10.76.7', port=8777):
        """
	Create the lights client listening on local_ip,port
	Set it up to send commands to ip_address,port
	Defaults work fine with example sketch.   Change for testing, etc...
        """
        self.ip = ip_address
        self.port = port
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock.bind((local_ip, port))


    def indicate_ball(self):
        message = '{ "sender" : "spill", "clear" : 1, "frect":[12,2,18,12,1]}'
        self.send_message(message)

    def indicate_target(self, angle):
        if -10 <= angle and angle <= -2:
            message = '{ "sender" : "spill", "clear" : 2, "frect":[2,2,8,12,4]}'
        if -2 < angle and angle < 2:
            message = '{ "sender" : "spill", "clear" : 3, "frect":[12,2,18,12,3]}'
        if 2 <= angle and angle <= 10:
            message = '{ "sender" : "spill", "clear" : 4, "frect":[22,2,28,12,2]}'      
        self.send_message(message)
    
    def send_message(self, message):
        self.send_sock.sendto(message.encode(), (self.ip, self.port))

    def test_all(self):
        pos = 0
        sleep_time = 0.01
        for color in range(5):
            message_dict = { "sender" : "spill", "clear" : 0, "frect":[pos,2,4+pos,12,color]}
            pos += 6
            message = str(message_dict)
            self.send_message(message)
            time.sleep(sleep_time)

        
