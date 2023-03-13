import communicate


NO_EVENT = 0
EVENT1 = 1
EVENT2 = 2
EVENT3 = 3
EVENT4 = 4


class EventController:
	def __init__(self):
		self.__event_signal_observers = []

		self.event = NO_EVENT

	def change_event(self, event):
		self.event = event
		if event != self.event:
			self.emit_event_change_signal()

	def get_event(self):
		return self.event

	def register_event_change_signal(self, observer):
		self.__event_signal_observers.append(observer)

	def deregister_event_change_signal(self, observer):
		if observer in self.__event_signal_observers:
			self.__event_signal_observers.remove(observer)

	def emit_event_change_signal(self):
		for observer in self.__event_signal_observers:
			observer(self.event)
