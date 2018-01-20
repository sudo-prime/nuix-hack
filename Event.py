class Event(object):
	def __init__(self, *args):
		self.args = args
		self.subcribers = set()

	def add(self, func):
		self.subscribers.add(func)

	def remove(self, func):
		self.subscribers.remove(func)

	def __call__(self, *args):
		runtime_args = self.args + args
		for subscriber in self.subscribers:
			subscriber(*runtime_args)
