import rpyc


class JarvisClient(object):

    def __init__(self, port, hostname='localhost'):
        self.conn = rpyc.connect(hostname, port)

    def sms_to_admin(self, text):
        return self.conn.root.sms_to_admin(text)

    def test(self):
        return print(self.conn.root.config())


if __name__ == '__main__':
    client = JarvisClient(54321)
    client.test()
