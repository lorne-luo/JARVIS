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


## How to run RPYC server
--------------------
    python server.py


## How to run RPYC client
--------------------
    from jarvis.client from JarvisClient
    client = JarvisClient(hostname='localhost', port=54321)
    client.sms_admin('test message',from_app='TEST')
    
    
## How to run GRPC server
```
python grpc_server.py
```

## Call from client
```
from jarvis.grpc.client import sms_admin
import threading
my_thread = threading.Thread(target=sms_admin,args=['test msg!','TEST'])
my_thread.start()
return_value = my_thread.join(2)
```
Contributing
------------

TBD

Example
-------

TBD
