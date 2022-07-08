ELEVATORS_PER_COLUMNS = [3, 3, 3, 3] # this array must contain 4 numbers n such that 3 <= n <= 5


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
    # |      | * The topmost elevator can't go from the last to the first floor             | #
    # | NOTE | * The bottommost elevator can't go from the first floor to the last          | #
    # |      | * Every elevator can go from self.count_below() to 300 - self.count_above()  | #
    # |______|______________________________________________________________________________| #
    def go_to(self, floor):
        if self.floor < floor:
            # Is this elevator the topmost one?
            if not self.above is None:
                # Are the elevetors above blocking its way?
                if self.above.floor <= floor:
                    # Recursively move the elevators blocking its way
                    self.above.go_to(floor + 1)

        elif self.floor > floor:
             # Is this elevator the bottommost one?
            if not self.below is None:
                # Are the elevetors below blocking its way?
                if self.below.floor >= floor:
                    # Recursively move the elevators blocking its way
                    self.below.go_to(floor - 1)
        self.floor = floor

    #  ____________________________________________________________________________________  #
    # | Count how many steps all the elevators should be moving in order for this elevator | #
    # | to get to its destination                                                          | #
    # |____________________________________________________________________________________| #
    def count_steps(self, floor):
        steps = 0
        if self.floor < floor:
            # Is this elevator the topmost one?
            if not self.above is None:
                # Are the elevetors above blocking its way?
                if self.above.floor <= floor:
                    # Recursively move the elevators blocking its way
                    steps += self.above.count_steps(floor + 1)

        elif self.floor > floor:
             # Is this elevator the bottommost one?
            if not self.below is None:
                # Are the elevetors below blocking its way?
                if self.below.floor >= floor:
                    # Recursively move the elevators blocking its way
                    steps += self.below.count_steps(floor - 1)

        return steps + abs(floor - self.floor)
                

#############################################################################################
#############################################################################################
#############################################################################################


def generate_elevators():
    elevators = []
    for i in range(4):
        col = []
        for e in range(ELEVATORS_PER_COLUMNS[i]):
            elev = Elevator(i, e)
            # Set above attribute for previous elevator
            # Set below attribute for current elevator 
            if e > 0:
                elev.below = col[e-1]
                col[e-1].above = elev
            
            col.append(elev)
    
        elevators.append(col)

    return elevators


# Prints elevators column and floor
def show_elevators(elevators):
    for col in elevators:
        for e in col:
            print(e)


# Display elevators in a matrix format
def elevator_matrix(elevators):
    for j in range(4, -1, -1):
        for i in range(4):
            try:
                print(f'{elevators[i][j].floor}', end='\t')
            except IndexError:
                print('', end='\t')
        print()


# Makes a copy of the elevators
def copy_elevators(elevators):
    copy = []
    for col in elevators:
        c = []
        for i, e in enumerate(col):
            elev = Elevator(e.col, e.floor)
            # Set above attribute for previous elevator
            # Set below attribute for current elevator 
            if i > 0:
                elev.below = c[i-1]
                c[i-1].above = elev

            c.append(elev)
        copy.append(c)
    
    return copy


#  ___________________________________________________________________  #
# | Needs to select the nearest elevator that will minimize steps to  | #
# | go to the desired floor accounting for the other elevators that   | #
# | might have to be moved in order to get the chosen elevator to its | #
# | destination                                                       | #
# |___________________________________________________________________| #
def call_elevator(floor_from, floor_to, elevators):
    if floor_from > 300 or floor_from < 0 or floor_to > 300 or floor_to < 0:
        raise ValueError

    nearest = (None, 10e6)
    # Making a copy
    copy = copy_elevators(elevators)

    # Get nearest elevator
    for i, col in enumerate(copy):
        for j, e in enumerate(col):
            # Calculate elevator steps to come and go
            steps = e.count_steps(floor_from) # Caluculate steps to take the passenger
            e.go_to(floor_from) # Move elevators 
            steps += e.count_steps(floor_to) # Calculate steps to go to the desired floor
            e.go_to(floor_to) # Move elevators 
           # Check that no elevator goes to negatives floors or floors above 300
            # then Reset elevators to its previous state
            for k, E in enumerate(elevators[i]):
                # Check for impossibles floors
                if col[k].floor > 300 or col[k].floor < 0:
                    print('illegal')
                    steps = 10e6
                # Reset floor
                col[k].floor = E.floor

            # Updating shortest path
            if nearest[1] > steps:
                nearest = (elevators[i][j], steps)

    nearest[0].go_to(floor_from)
    nearest[0].go_to(floor_to)
    elevator_matrix(elevators)



if __name__ == '__main__':
    elevators = generate_elevators()
    elevator_matrix(elevators)
    while True:
        try:
            from_ = int(input('[+] Enter your current floor: '))
            to = int(input('[+] Enter the floor where you want to go to: '))
            call_elevator(from_, to, elevators)
        except ValueError:
            print('\n[!] Input must be a number between 0 and 300!\n')
        except KeyboardInterrupt:
            print('\n[.] Exiting')
            exit()
        except EOFError:
            print('\n[.] Exiting')
            exit()
