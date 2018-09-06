# encoding=utf-8
__author__ = 'kevinlu1010@qq.com'
'''
进程间通信
'''
from multiprocessing.managers import BaseManager
from multiprocessing import RLock

MANAGER_PORT = 6000
MANAGER_DOMAIN = '0.0.0.0'
MANAGER_AUTH_KEY = b'aaaaaaaaaaaaaaa'

#定义一个Manager类
class InfoManager(BaseManager): pass


class DictItem():
    def __init__(self, ):
        self.items = dict()

    def set(self, key, value):
        self.items[key] = value

    def get(self, key):
        return self.items.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

#为这个manager类注册存储容器，也就是通过这个manager类实现的共享的变量，
#这个变量最好是一个类实例，自己定义的或者python自动的类的实例都可以
#这里不能把d改成dict()，因为Client那边执行d['keyi']='value'的时候会报错：d这个变量不能修改
d = DictItem()
lock = RLock()
InfoManager.register('dict', callable=lambda: d)
InfoManager.register('open_qq_login_lock', callable=lambda: lock)


class ManagerServer():
    '''
    multiprocess Manager服务类
    '''

    def __init__(self, domain, port, auth_key):
        self.domain = domain
        self.port = port
        self.auth_key = auth_key

    def start_manager_server(self):
        self.queue_manager = InfoManager(address=('', self.port), authkey=self.auth_key)
        # self.dict = self.queue_manager.dict()
        self.server = self.queue_manager.get_server()

    def run(self):
        self.start_manager_server()
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.is_stop = 1


class ManagerClient():
    '''
    访问mutiprocess Manager的类
    '''

    def __init__(self, domain, port, auth_key):
        self.domain = domain
        self.port = port
        self.auth_key = auth_key
        # self.get_share_dict()
        self.info_manager = InfoManager(address=(self.domain, self.port), authkey=self.auth_key)
        self.info_manager.connect()

    def get_dict(self):
        # self.dict = m.dict()
        self.dict = self.info_manager.dict()
        return self.dict

    def get_open_qq_login_lock(self):
        self.open_qq_login_lock = self.info_manager.open_qq_login_lock()
        return self.open_qq_login_lock


if __name__ == '__main__':
    server = ManagerServer(MANAGER_DOMAIN, MANAGER_PORT, MANAGER_AUTH_KEY)
    server.run()
