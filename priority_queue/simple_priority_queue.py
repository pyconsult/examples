#!/usr/bin/env python


import heapq

from collections import namedtuple

# A named tuple that is sorted using the 'timestamp' filed because it is the
# first entry.
MessageEntry = namedtuple('MessageEntry',
                          ['timestamp', 'message'],)


class MessagePriorityQueue():
    def __init__(self):
        self.data = []

    def push(self, entry):
        heapq.heappush(self.data, entry)

    def pop(self):
        return heapq.heappop(self.data)


if __name__ == '__main__':

    # make an unordered list of message entries
    message_entry_list = []
    for i in [1, 3, 5, 4, 2, 6, 3, 10, 9]:
        message_entry_list.append(MessageEntry(timestamp=i, message=i))

    queue = MessagePriorityQueue()

    for message_entry in message_entry_list:
        queue.push(message_entry)

    for i in range(len(queue.data)):
        print queue.pop()



    



