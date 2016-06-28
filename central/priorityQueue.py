# import Queue;

class PriorityQueue(object):

	def __init__(self):
		self.queue = [];

	def qsize(self, len=len):
		return len(self.queue);

	def empty(self):
		return len(self.queue) == 0;

	def put_l2h(self, item):
		data,priority = item;
		self._insort_right((priority, data));
	
	def put_h2l(self, item):
		data,priority = item;
		self._insort_left((priority, data));
	
	def remove(self, instId):	# remove by instId which is wierd but we have no choice
		for i in range(0, len(self.queue)):
			if( self.queue[i][1][0] == instID):
				self.queue.pop(i);
		assert False

	def update(self, inst, idx):
		assert idx < len(self.queue);
		self.queue[idx][1][6] = inst[6];

	def peek(self):
		return list(self.queue[0][1]);

	def get(self):
		return self.queue.pop(0)[1];	# (priority, data)
	
	def _insort_right(self, x):
		"""Insert item x in list, and keep it sorted from low to high assuming a is sorted.
		If x is already in list, insert it to the right of the rightmost x.       
		"""
		a = self.queue
		lo = 0        
		hi = len(a)

		while lo < hi:
			mid = (lo+hi)/2
			if x[0] < a[mid][0]: hi = mid
			else: lo = mid+1
		a.insert(lo, x)
	
	def _insort_left(self, x):
		"""Insert item x in list, and keep it sorted from high to low assuming a is sorted.
		If x is already in list, insert it to the right of the rightmost x.       
		"""
		a = self.queue
		lo = 0        
		hi = len(a)

		while lo < hi:
			mid = (lo+hi)/2
			if x[0] > a[mid][0]: hi = mid
			else: lo = mid+1
		a.insert(lo, list(x))

def test():
	pq = PriorityQueue()

	pq.put_h2l(('b', 1.23))
	pq.put_h2l(('a', 1))
	pq.put_h2l(('c', 1))
	pq.put_h2l(('z', 0))
	pq.put_h2l(('d', 2))
	print(pq.qsize())
	while not pq.empty():
		print(pq.get())

# test() 
