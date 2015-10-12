#!/usr/bin/env python


import heapq

from collections import namedtuple

# A named tuple that is sorted using the 'timestamp' filed because it is the
# first entry.
MessageEntry = namedtuple('MessageEntry',
                          ['timestamp', 'message'],)


class BoundedPriorityQueue():
    def __init__(self, maxlen=3):
        self.data = []
        self.maxlen = maxlen

    def push(self, entry):
        if len(self.data) >= self.maxlen:
            return heapq.heappushpop(self.data, entry)
        return heapq.heappush(self.data, entry)

    def pop(self):
        return heapq.heappop(self.data)


if __name__ == '__main__':

    # make an unordered list of message entries
    message_entry_list = []
    for i in [1, 3, 5, 4, 2, 6, 3, 10, 9]:
        message_entry_list.append(MessageEntry(timestamp=i, message=i))

    queue = BoundedPriorityQueue()

    print "pushing messages onto queue"
    for message_entry in message_entry_list:
        print queue.push(message_entry)

    print "last messages"
    for i in range(len(queue.data)):
        print queue.pop()

