import rpyc


class JarvisClient(object):

    def __init__(self, port, hostname='localhost'):
        self.conn = rpyc.connect(hostname, port)

    def sms_admin(self, text, from_app=None):
        return self.conn.root.sms_admin(text, from_app)

    def test(self):
        return print(self.conn.root.config())


if __name__ == '__main__':
    client = JarvisClient(54321)
    client.test()
