from kazoo.client import KazooClient


zk = KazooClient(hosts='zoo1:2181')


def init_zookeeper():
    print("zk start")
    zk.start()
    print("zk start finish")


class ConnManager:
    def __init__(self) -> None:
        self.conn_count = 0

    @property
    def count(self):
        return self.conn_count

    def add_conn(self):
        self.conn_count = self.conn_count + 1

    def remove_conn(self):
        self.conn_count = self.conn_count - 1

cm = ConnManager()
