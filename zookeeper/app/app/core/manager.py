from kazoo.client import KazooClient


zk = KazooClient(hosts='zoo1:2181')


def init_zookeeper():
    print("zk start")
    zk.start()
    print("zk start finish")
