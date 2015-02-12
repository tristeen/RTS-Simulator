class Camp(object):
	
	def __init__(self, _id, _color):
		self.id_ = _id
		self.res_ = 7
		#self.units_ = []
		self.color_ = _color

#	def add_unit(self, _unit):
#		self.units_.append(_unit.id)
#
#	def del_unit(self, _unit):
#		if _unit.id in self.units_:
#			self.units_.remove(_unit.id)

	def add_res(self, _res):
		self.res_ += _res
		
	def sub_res(self, _res):
		self.res_ -= _res

	def to_dict(self):
		return self.__dict__

	def from_dict(self, d):
		self.__dict__.update(d)
