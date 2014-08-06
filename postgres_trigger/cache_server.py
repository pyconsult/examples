#!/usr/bin/python
 
import logging
 
import gevent
import zmq.green as zmq
import json
 
LOG = logging.getLogger(__name__)
 
 
context = zmq.Context()


class Server(gevent.Greenlet):
    """Simple server that receives data from database triggers """
 
    def __init__(self, port='9999'):
        super(Server, self).__init__()
        self.port = port
        self.cached_counter = 0
 
    def _run(self):
        """
        Runs a simple server that broadcasts its existance via udp and the
        broadcast class.
 
        """
        LOG = logging.getLogger("cache-server.%s" %
                                self.__class__.__name__)
 
        # connect to trigger port
        incoming = context.socket(zmq.PULL)
        incoming.connect("tcp://127.0.0.1:%s" % self.port)

        # listen for connections to cache 
        cache_req = context.socket(zmq.REP)
        cache_req.bind("tcp://127.0.0.1:8888")
 
        # poll for new messages from the database 
        db_poller = zmq.Poller()
        db_poller.register(incoming, zmq.POLLIN)
        
        # poll for new cache requests
        cache_req_poller = zmq.Poller()
        cache_req_poller.register(cache_req, zmq.POLLIN)
 
        try:
            while True:
                
                # listen for connections from databse and update cache
                db_events = dict(db_poller.poll(1000*1))
                if len(db_events) != 0:
                    message = incoming.recv()
                    TD = json.loads(message)
                    LOG.info("got client message: %s" % message)
                    LOG.debug("Old cached value %s", self.cached_counter)
                    if TD['event'] == 'INSERT':
                        self.cached_counter += int(TD['new']['count'])
                    elif TD['event'] == 'UPDATE':
                        self.cached_counter -= int(TD['old']['count'])
                        self.cached_counter += int(TD['new']['count'])
                    elif TD['event'] == 'DELETE':
                        self.cached_counter -= int(TD['old']['count'])
                    LOG.debug("New cached value %s", self.cached_counter)
               
                # listed for cache requests 
                cache_events = dict(cache_req_poller.poll(1000*1))
                if len(cache_events) != 0:
                    message = cache_req.recv()
                    if message == 'whats up ?':
                        response = self.cached_counter
                        cache_req.send(str(response))

                ##gevent.sleep(1)
 
        # Handle shutdown by closing sockets
        finally:
            LOG.info("Shutting down server")
            incoming.close()
            cache_req.close()

def main():
    """docstring for main"""
 
    server = Server()
    server.start()
 
    # only wait for the server to finish
    gevent.joinall([server, ])
 
 
if __name__ == '__main__':
    LOG = logging.getLogger("database-trigger-server")
    logging.basicConfig(level=logging.DEBUG)
    main()
 
