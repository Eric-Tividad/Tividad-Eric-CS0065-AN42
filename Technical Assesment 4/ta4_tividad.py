# RULE-BASED REASONING SECTION
# The knowledge base: "player" stats
facts = {
    "status": {
        "health": 70, # out of 100
        "hunger": 75, # out of 100, higher = hungrier
        "is_bitten": False,
    },
    "supplies": {
        "ammo": 3,
        "water_bottles": 0,
        "has_medkit": True,
    },
    "surroundings": {
        "zombies_nearby": 12,
        "is_night": True,
        "in_shelter": False,
        "has_vehicle": False,
    },
}

# low health & has medkit = heal bradar
def rule_low_health(facts):
    if facts["status"]["health"] < 50 and facts["supplies"]["has_medkit"]:
        return "Use the medkit to heal"

# hungry = look for food pls
def rule_hungry(facts):
    if facts["status"]["hunger"] > 70:
        return "Scavenge for food"

# no water = look for water source 
def rule_no_water(facts):
    if facts["supplies"]["water_bottles"] == 0:
        return "Find a clean water source"

# surrounded by zombies & low ammo = don't fight
def rule_surrounded(facts):
    if facts["surroundings"]["zombies_nearby"] > 10 and facts["supplies"]["ammo"] < 5:
        return "Avoid combat and run or hide"

# night time and not in shelter = look for shelter
def rule_night(facts):
    if facts["surroundings"]["is_night"] and not facts["surroundings"]["in_shelter"]:
        return "Find a shelter first"

# bitten = gtfo of the group
def rule_bitten(facts):
    if facts["status"]["is_bitten"]:
        return "Isolate yourself from the group"

# surrounding has vehicles and not many zombie is arround = USE THE VEHICLE BRADAR
def rule_vehicle(facts):
    if facts["surroundings"]["has_vehicle"] and facts["surroundings"]["zombies_nearby"] > 0:
        return "Escape using the vehicle"
 
# list of all the rules
rules = [rule_low_health, rule_hungry, rule_no_water, rule_surrounded,
         rule_night, rule_bitten, rule_vehicle]

# the inference machine!
# runs all rules function then stores it in a array
def inference_engine(facts, rules):
    actions = []
    for rule in rules:
        result = rule(facts)
        if result is not None:
            actions.append(result)
    return actions

# CASE-BASED REASONING SECTION
# (the case base is made before the loop so saved cases are kept every round)
case_base = [
    {"problem": {"zombies_nearby": "many", 
                 "ammo": "low", 
                 "in_shelter": False, 
                 "is_night": True
                 },
     "solution": "Sneak away quietly and hide in a building until sunrise."
     },

    {"problem": {"zombies_nearby": "few", 
                 "ammo": "high", 
                 "in_shelter": False, 
                 "is_night": False
                 },
     "solution": "Clear the zombies with controlled shots and loot the area."
     },

    {"problem": {"zombies_nearby": "many", 
                 "ammo": "high", 
                 "in_shelter": True, 
                 "is_night": True
                 },
     "solution": "Barricade the doors and shoot from the windows."
     },

    {"problem": {"zombies_nearby": "few",
                 "ammo": "low", 
                 "in_shelter": True, 
                 "is_night": False
                 },
     "solution": "Stay put, rest, and craft melee weapons."
     },
]

# similarity check 
def similarity(new_problem, old_problem):
    matches = 0
    for feature in new_problem:
        if new_problem[feature] == old_problem[feature]:
            matches = matches + 1
    return matches / len(new_problem)


# MAIN LOOP: runs RBR, then CBR, then asks if the user wants to go again
while True:
    print("Zombie Apocalypse Survival Guide")
    print("PLAYER STATS:")
    for category in facts:
        print("[" + category + "]")
        for name in facts[category]:
            print("  " + name + ": " + str(facts[category][name]))
    print()

    # just prints out the possible actions based from the rules and facts we have
    actions = inference_engine(facts, rules)
    print("Rule-Based Reasoning Actions:")
    if len(actions) == 0:
        print("- No rules fired")
    for action in actions:
        print("- " + action)
    print()

    print("Describe your situation:")
    zombies = input("How many zombies are nearby? (few/many): ").strip().lower()
    ammo = input("How is your ammo? (low/high): ").strip().lower()
    shelter = input("Are you in a shelter? (yes/no): ").strip().lower()
    night = input("Is it night? (yes/no): ").strip().lower()

    new_problem = {
        "zombies_nearby": zombies,
        "ammo": ammo,
        "in_shelter": shelter == "yes",
        "is_night": night == "yes",
    }

    # the 4R's of CBR!
    # RETRIEVE: Finds the most similar case for the new case
    print("")
    print("Case-Based Reasoning Solution")
    print("Checking similarity with other cases:")
    best_case = None
    best_score = -1
    number = 1
    for case in case_base:
        score = similarity(new_problem, case["problem"])
        print("Similarity with case " + str(number) + ": " + str(round(score, 2)))
        if score > best_score:
            best_score = score
            best_case = case
        number = number + 1

    # REUSE: use the solution of the best case
    solution = best_case["solution"]
    print("Proposed solution: " + solution)

    # REVISE: the user can change the solution
    print("")
    answer = input("Would you like to change the proposed solution? (y/n): ").strip().lower()

    if answer == "y":
        new_solution = input("Enter new solution (or Enter to keep it): ").strip()
        if new_solution != "":
            solution = new_solution
            print("Solution changed")
        else:
            print("Nothing entered, solution kept")
    else:
        print("Solution accepted")

    # RETAIN: save the new case so it can be used next time
    case_base.append({"problem": new_problem, "solution": solution})
    print("Case saved. The case base now has " + str(len(case_base)) + " cases.")
    print("\nFinal solution: " + solution)

    # ask if the user wants to run again or quit
    print("")
    again = input("Run again or quit? (y/n): ").strip().lower()
    while again != "y" and again != "n":
        again = input("Please type y to run again or n to quit: ").strip().lower()
    if again == "n":
        print("Stay alive out there!")
        break
    print("------------------------------")