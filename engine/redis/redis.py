import redis


class RedisSentinel:
    def __init__(self, sentinel_list, name, password="", db=0):
        self.sentinel = redis.Sentinel(sentinel_list, socket_timeout=60)
        self.name = name
        self.password = password
        self.db = db

    def get_master_and_slave_conn(self):
        master = self.sentinel.master_for(
            service_name=self.name,
            socket_timeout=60,
            password=self.password,
            db=self.db)
        slave = self.sentinel.slave_for(
            service_name=self.name,
            socket_timeout=60,
            password=self.password,
            db=self.db
        )
        return master, slave


redis_sentinel = RedisSentinel(config.SENTINEL_NODES, config.MASTER_NAME, config.SENTINEL_PASSWORD, 0)
redis_master, redis_slave = redis_sentinel.get_master_and_slave_conn()
redis_sentinel1 = RedisSentinel(config.SENTINEL_NODES, config.MASTER_NAME, config.SENTINEL_PASSWORD, 1)
redis_master1, redis_slave1 = redis_sentinel1.get_master_and_slave_conn()
