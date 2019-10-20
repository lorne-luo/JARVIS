import rpyc
from environs import Env

env = Env()
env.read_env()

JARVIS_HOST = env.str('JARVIS_HOST', default='localhost')
JARVIS_PORT = env.int('JARVIS_PORT', default=54321)


class JarvisClient(object):

    def __init__(self, hostname='localhost', port=54321):
        self.conn = rpyc.connect(hostname, port)

    def sms_admin(self, message, from_app=None):
        return self.conn.root.sms_admin(message, from_app)

    def telegram_jarvis(self, message, from_app=None):
        return self.conn.root.telegram_jarvis(message, from_app)


jarvis = JarvisClient(port=JARVIS_PORT, hostname=JARVIS_HOST)

if __name__ == '__main__':
    client = JarvisClient(port=54321)
    client.telegram_jarvis('test message!')
