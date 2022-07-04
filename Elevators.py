class Elevator:
	def __init__(self, col, floor):
		self.col = col
		self.floor = floor
		self.above = None # An elevator
		self.below = None # An elevator


	def __str__(self):
		return f'Elevator at column {self.col} and floor {self.floor}'

	# Checks if the elevator is the one on top of all of the others
	def is_highest(self):
		if self.above is None:
			return True
		return False

	# Checks if the elevator is the one on the bottom of all of the others
	def is_lowest(self):
		if self.below is None:
			return True
		return False

 	# Counts how many elevators there are above this elevator
	def count_above(self):
		if self.is_highest:
			return 0
		else:
			count = 0
			nxt = self.above
			while not nxt.above is None:
				count += 1
				nxt = nxt.above

			return count

	# Counts how many elevators there are below this elevator
	def count_below(self):
		if self.is_lowest:
			return 0
		else:
			count = 0
			nxt = self.below
			while not nxt.belowe is None:
				count += 1
				nxt = nxt.below

			return count

	#  _____________________________________________________________________________________  #
	# |      | * The topmost elevator can't go from the last to the first floor				| #
	# | NOTE | * The bottommost elevator can't go from the first floor to the last			| #
	# |      | * Every elevator can go from self.count_below() to 300 - self.count_above()	| #
	# |______|______________________________________________________________________________| #
	def go_to(self, floor):
		if self.floor < floor:
			# If this elevator is the one on top of all just go up
			if self.is_highest:
				self.floor = floor
			# Check if the elevator above is on the way
			else if self.above.floor < floor:
				self.floor = floor
			else:
				# | Need to move the elevator blocking the way upward to floor + 1 | #
				# | And recursevively move the other that may be blocking the way  | #
				print('There is an elevator blocking the way')

		elif self.floor > floor:
			# If this elevator is the one on the bottom of all just go up
			if self.is_lowest:
				self.floor = floor
			# Check if the elevator above is on the way
			else if self.below.floor > floor:
				self.floor = floor
			else:
				# | Need to move the elevator blocking the way downward to floor - 1 | #
				# | and recursevively move the other that may be blocking the way    | #
				print('There is an elevator blocking the way')


				
				
def generate_elevators(n=3):
	elevators = []
	for i in range(4):
		col = []
		for e in range(n):
			elev = Elevator(i, e)
			# Set above attribute for previous elevator
			# Set below attribute for current elevator 
			if e > 0:
				elev.below = col[e-1]
				col[e-1].above = elev
			
			col.append(elev)
	
		elevators.append(col)

	return elevators


def show_elevators(elevators):
	for col in elevators:
		for e in col:
			print(e)


elevators = generate_elevators()
show_elevators(elevators)
