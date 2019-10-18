JARVIS
===============================

version number: 0.0.1
author: Lorne Luo

Overview
--------

Notification micro services by SMS, EMail, Telegram, Weixin

Installation / Usage
--------------------

To install use pip:

    $ pip install jarvis


Or clone the repo:

    $ git clone https://github.com/lorne-luo/jarvis.git
    $ python setup.py install


How to run RPYC server
--------------------
    python server.py


How to run RPYC client
--------------------
    from jarvis.client from JarvisClient
    client = JarvisClient(hostname='localhost', port=54321)
    client.sms_admin('test message',from_app='TEST')
    

Contributing
------------

TBD

Example
-------

TBD