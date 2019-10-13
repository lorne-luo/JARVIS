import rpyc
from environs import Env

env = Env()
env.read_env()

JARVIS_HOST = env.str('JARVIS_HOST', default='localhost')
JARVIS_PORT = env.int('JARVIS_PORT', default=54321)


class JarvisClient(object):

    def __init__(self, port, hostname='localhost'):
        self.conn = rpyc.connect(hostname, port)

    def sms_admin(self, text, from_app=None):
        return self.conn.root.sms_admin(text, from_app)

    def test(self):
        return print(self.conn.root.config())


jarvis = JarvisClient(port=JARVIS_PORT, hostname=JARVIS_HOST)

if __name__ == '__main__':
    client = JarvisClient(54321)
    client.test()
