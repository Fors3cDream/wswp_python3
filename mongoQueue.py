from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MongoQueue:
    # possilbe states of a download
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        """

        :param client: MongoDB server IP address
        :param timeout:
        """
        self.client = MongoClient() if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    def __nonzero__(self):
        """
        Returns true if there are more jobs to process
        :return:
        """
        record = self.db.crawlQueue.find_one(
            {'status':{'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url):
        """
        Add new url to queue if does not exist
        :param url:
        :return:
        """
        try:
            self.db.crawlQueue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass

    def pop(self):
        """
        Get an outstanding url from the queue and set its status to processing.
        If the queue is empty a KeyError exception is raised.
        :return:
        """
        record = self.db.crawlQueue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )

        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def peek(self):
        record = self.db.crawlQueue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.crawlQueue.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """
        Release stalled jobs
        :return:
        """
        record = self.db.crawlQueue.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )

        if record:
            print('Released:', record['_id'])

    def clear(self):
        self.db.crawlQueue.drop()