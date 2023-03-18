EVENT_CONTROLLER = None


def get_event_controller():
	global EVENT_CONTROLLER
	if not EVENT_CONTROLLER:
		EVENT_CONTROLLER = EventController()
	return EVENT_CONTROLLER


class EventController:
	def __init__(self):
		self.__event = []

	def create_event(self, name, value_type, observer_func=None):
		event_obj = Event(name, value_type, observer_func)
		self.__event.append(event_obj)
		return event_obj

	def change_event(self, name, value):
		event = self.get_event(name)
		if event:
			event.set_value(value)

	def get_event(self, name):
		for event in self.__event:
			if event.name == name:
				return event
		raise ValueError('Event {} is does not exist'.format(name))

	def register_event_change_signal(self, name, observer):
		event = self.get_event(name)
		if event:
			event.register_observer(observer)

	def deregister_event_change_signal(self, name, observer):
		event = self.get_event(name)
		if event:
			event.deregister_observer(observer)


class Event:
	def __init__(self, name, value_type, observer_func=None):
		self.name = name
		self.value_type = value_type
		self.value = None
		self.observer = [observer_func] if observer_func else []
	
	def set_value(self, value):
		if type(value) != self.value_type:
			raise ValueError('Event type error, event value should be {}'.format(self.value_type))
		
		# emit signal
		if value != self.value:
			self.value = value
			for observer in self.observer:
				observer(self)
			return True
		
		return False
	
	def register_observer(self, observer_func):
		self.observer.append(observer_func)
	
	def deregister_observer(self, observer_func):
		self.observer.remove(observer_func)
		



