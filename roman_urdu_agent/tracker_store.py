# this tracker class is not being used for now !
# read more at 'tracker_store' in endpoint.yml
from rasa.core.tracker_store import TrackerStore


class RedisTrackerStore(TrackerStore):

    def keys(self):
        pass

    def __init__(self, domain, host='localhost',
                 port=6379, db=0, password=None):

        import redis
        self.red = redis.StrictRedis(host=host, port=port, db=db,
                                     password=password)
        super(RedisTrackerStore, self).__init__(domain)

    def save(self, tracker, timeout=None):
        serialised_tracker = self.serialise_tracker(tracker)
        self.red.set(tracker.sender_id, serialised_tracker, ex=timeout)

    def retrieve(self, sender_id):
        stored = self.red.get(sender_id)
        if stored is not None:
            return self.deserialise_tracker(sender_id, stored)
        else:
            return None
