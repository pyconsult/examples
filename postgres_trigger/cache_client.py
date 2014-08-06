#!/usr/bin/python
 
import logging
import zmq.green as zmq


LOG = logging.getLogger("client-cache")
logging.basicConfig(level=logging.DEBUG)

context = zmq.Context()

LOG.debug("connecting to server")
outgoing = context.socket(zmq.REQ)
outgoing.connect('tcp://127.0.0.1:8888')

try:
    outgoing.send('whats up ?')
    
    # Receive the reply from the service and print it
    reply = outgoing.recv()
    LOG.info("got response %s" % reply)

finally:
    # always close zmq socket
    outgoing.close()


 
