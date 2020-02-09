import heapq


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def push(self, data):
        heapq.heappush(self.queue, data)  # todo: (node, cost/weight)

    def pop(self):
        return heapq.heappop(self.queue)