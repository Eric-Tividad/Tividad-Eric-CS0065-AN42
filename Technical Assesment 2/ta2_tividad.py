import random

# task 1
# two rooms: A and B
rooms = {"A": "Clean", "B": "Clean"}

# checks if a room is dirty
def is_dirty(room):
    if rooms[room] == "Dirty":
        return True
    return False

# cleans a room
def clean(room):
    rooms[room] = "Clean"
    print("I am cleaning the room")

# task 2
class Agent:
    def __init__(self):
        self.location = "A"   # agent always starts in room A

    # moves to another room
    def move(self):
        if self.location == "A":
            self.location = "B"
        else:
            self.location = "A"

    def perceive_and_act(self):
        # room dirty = clean it
        if is_dirty(self.location):
            clean(self.location)
            print("Room " + self.location + " has been cleaned.")

        # room is clean = move to other
        else:
            self.move()
            print("Moving to room " + self.location)

# for running basic simulation
def run_basic():
    # ask the user for the starting state of each room
    for r in rooms:
        state = input("Is room " + r + " Dirty or Clean? ")
        rooms[r] = state.strip().capitalize()

    steps = int(input("\nHow many steps should the agent run? "))

    agent = Agent()

    for i in range(1, steps + 1):
        print("\nStep " + str(i) + ": Agent is in room " + agent.location)
        agent.perceive_and_act()
        print("Environment state:", rooms)


# bonus task section
rooms3 = {"A": "Clean", "B": "Clean", "C": "Clean"}

# new agent class for the bonus simulation
class Agent3:
    def __init__(self):
        self.location = "A"   # starts in room A again

    # same logic on the first agent; just moves randomly on the three rooms to clean it
    def perceive_and_act(self):
        # room is dirty = clean it
        if rooms3[self.location] == "Dirty":
            rooms3[self.location] = "Clean"
            print("Room " + self.location + " has been cleaned.")
        else:
            # perceive and collect dirty rooms for random picking
            dirty_rooms = []
            for r in rooms3:
                if rooms3[r] == "Dirty":
                    dirty_rooms.append(r)

            if len(dirty_rooms) > 0:
                self.location = random.choice(dirty_rooms)
                print("Moving to room " + self.location)
            else:
                # all rooms are cleaned!
                print("All rooms are clean. Agent is idle")

 # prints the rooms like [A-Agent]  [B-Dirty]  [C-Clean]
def show_grid(location):
    line = ""
    for r in rooms3:
        if r == location:
            line += "[" + r + "-Agent]  "
        else:
            line += "[" + r + "-" + rooms3[r] + "]  "
    print(line)

 # runs bonus simulation
def run_bonus():
    for r in rooms3:
        state = input("Is room " + r + " Dirty or Clean? ")
        rooms3[r] = state.strip().capitalize()
 
    steps = int(input("\nHow many steps should the agent run? "))
 
    agent = Agent3()
 
    for i in range(1, steps + 1):
        print("\nStep " + str(i) + ":")
        show_grid(agent.location)
        agent.perceive_and_act()
        show_grid(agent.location)

# ze menu
print("Technical Assesment 2: Rule-Based Agent")
print("1 - Two rooms")
print("2 - Three rooms (Bonus)")
choice = input("Pick a mode: ")
print()

if choice == "1":
    run_basic()
else:
    run_bonus()