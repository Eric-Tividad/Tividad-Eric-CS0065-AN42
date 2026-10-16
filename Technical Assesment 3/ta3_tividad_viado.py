# Steps of the program:
# 1. Similarity search                  - find the most similar past disaster for the new disaster
# 2. Solution adaptation                - adapt the old solution to the new problem
# 3. Solution adaptation: finalization  - user can either accept or change the solution
# 4. Final solution                     - save the new case in the case base

# past disasters we will use to compare
# each has a problem and solution dictionary, for attribute comparison stuff
# types: Typhoon, Flood, and Earthquakes
# area: Urban, Coastal, and Rural
# flood_risk: 1 - low, 2 - medium, 3 - high risk level
case_base = [
    {"name": "Typhoon Ursula (2019)",
     "problem": {"type": "Typhoon", 
                 "area": "Urban", 
                 "flood_risk": 3, 
                 "population": 60000},

     "solution": {"evacuees": 18000, 
                  "shelters": 6, 
                  "boats": 6, 
                  "relief_packs": 18000}},

    {"name": "Typhoon Odette (2021)",
     "problem": {"type": "Typhoon", 
                 "area": "Coastal", 
                 "flood_risk": 3, 
                 "population": 120000},

     "solution": {"evacuees": 48000, 
                  "shelters": 16, 
                  "boats": 12, 
                  "relief_packs": 48000}},

    {"name": "Flooding Ulysses (2020)",
     "problem": {"type": "Flood", 
                 "area": "Urban", 
                 "flood_risk": 3,
                 "population": 90000},

     "solution": {"evacuees": 27000, 
                  "shelters": 9, 
                  "boats": 10, 
                  "relief_packs": 27000}},

    {"name": "Flooding Ondoy (2009)",
     "problem": {"type": "Flood", 
                 "area": "Urban", 
                 "flood_risk": 3, 
                 "population": 150000},

     "solution": {"evacuees": 60000, 
                  "shelters": 20, 
                  "boats": 15, 
                  "relief_packs": 60000}},

    {"name": "Bohol Earthquake (2013)",
     "problem": {"type": "Earthquake", 
                 "area": "Rural", 
                 "flood_risk": 1, 
                 "population": 40000},

     "solution": {"evacuees": 12000, 
                  "shelters": 5, 
                  "boats": 0, 
                  "relief_packs": 12000}},

    {"name": "Moro Gulf Earthquake and Tsunami (1976)",
     "problem": {"type": "Earthquake", 
                 "area": "Coastal", 
                 "flood_risk": 3, 
                 "population": 90000},
 
     "solution": {"evacuees": 45000, 
                  "shelters": 15, 
                  "boats": 8, 
                  "relief_packs": 45000}}
]

# determines if the new typhoon is similar to the past typhoons
# similarity weight: type = 0.35, area = 0.25, flood risk = 0.20, population = 0.20
def get_similarity(new_problem, old_problem):
    score = 0

    # disaster type similarity
    if new_problem["type"] == old_problem["type"]:
        score = score + 0.35

    # area type similarity
    if new_problem["area"] == old_problem["area"]:
        score = score + 0.25

    # flood risk similarity (the closer, the higher)
    difference = abs(new_problem["flood_risk"] - old_problem["flood_risk"])
    score = score + 0.20 * (1 - difference / 2)

    # population similarity (the closer, the higher)
    smaller = min(new_problem["population"], old_problem["population"])
    bigger = max(new_problem["population"], old_problem["population"])
    score = score + 0.20 * (smaller / bigger)

    return score

print("TA3: Disaster Response Decision Support System")

while True:
    # the new disaster to analyze, the user types it in
    print("")
    print("ENTER THE NEW DISASTER TO PREPARE FOR:")

    # disaster type 
    while True:
        new_type = input("Disaster type (Typhoon/Flood/Earthquake): ").strip().capitalize()
        if new_type in ["Typhoon", "Flood", "Earthquake"]:
            break
        print("Please enter valid disaster type!")

    # area type 
    while True:
        new_area = input("Area type (Urban/Coastal/Rural): ").strip().capitalize()
        if new_area in ["Urban", "Coastal", "Rural"]:
            break
        print("Please enter valid area type!")

    # flood risk (1, 2, or 3 only)
    while True:
        risk_text = input("Flood risk (1 = Low, 2 = Medium, 3 = High): ").strip()
        if risk_text in ["1", "2", "3"]:
            new_risk = int(risk_text)
            break
        print("Please enter valid levels!")

    # population (whole number greater than 0, commas are removed)
    while True:
        population_text = input("Population (numbers only): ").strip().replace(",", "")
        if population_text.isdigit() and int(population_text) > 0:
            new_population = int(population_text)
            break
        print("Please enter a number greater than 0")

    new_problem = {"type": new_type, 
                   "area": new_area, 
                   "flood_risk": new_risk, 
                   "population": new_population}
    print("")
    print("NEW PROBLEM TO PREPARE FOR:")
    print("Disaster type: " + new_problem["type"])
    print("Area type: " + new_problem["area"])
    print("Flood risk: " + str(new_problem["flood_risk"]) + " (1 = Low, 2 = Medium, 3 = High)")
    print("Population: " + str(new_problem["population"]))

    # step 1: determine which typhoon is similar to the new one
    print("")
    print("DISASTER SIMILARITY SEARCH:")
    best_case = None
    best_score = -1

    for case in case_base:
        score = get_similarity(new_problem, case["problem"])
        print(case["name"] + " -> " + str(round(score, 2)))
        # keep the case with the highest score
        if score > best_score:
            best_score = score
            best_case = case

    print("")
    print("Most Similar Disaster: " + best_case["name"] + " (score: " + str(round(best_score, 2)) + ")")
    old_solution = best_case["solution"]
    print("Old solution: " + str(old_solution))

    # step 2: adapting the old solution to the new disaster
    print("")
    print("SOLUTION ADAPTATION:")

    # gets the population ratio of new and similar disaster
    ratio = new_problem["population"] / best_case["problem"]["population"]
    print("Population ratio: " + str(round(ratio, 2)))

    new_solution = {}
    new_solution["evacuees"] = round(old_solution["evacuees"] * ratio)
    new_solution["shelters"] = round(old_solution["shelters"] * ratio)
    new_solution["boats"] = round(old_solution["boats"] * ratio)
    new_solution["relief_packs"] = round(old_solution["relief_packs"] * ratio)

    # if the flood risk is higher than the old case, add 20% evacuees and boats
    if new_problem["flood_risk"] > best_case["problem"]["flood_risk"]:
        new_solution["evacuees"] = round(new_solution["evacuees"] * 1.2)
        new_solution["boats"] = round(new_solution["boats"] * 1.2)
        print("Flood risk is higher, evacuees and boats increased by 20%")

    print("Adapted solution: " + str(new_solution))

    # step 3: use or revise the provided solution
    print("")
    print("SOLUTION ADAPTATION: FINALIZATION:") 
    answer = input("Would like to change the new solution? (y/n): ").strip().lower()

    if answer == "y":
        for item in ["evacuees", "shelters", "boats", "relief_packs"]:
            number = input("Enter new " + item + " (Enter to keep " + str(new_solution[item]) + "): ").strip()
            if number.isdigit():
                new_solution[item] = int(number)
                print(item + " changed to " + number)
            elif number != "":
                print("Invalid number, " + item + " not changed")
    else:
        print("Solution accepted")

    print("")
    print("FINAL SOLUTION: " + str(new_solution))

    # step 4: final solution
    print("")
    print("FINAL SOLUTION FOR THE NEW DISASTER:")
    new_case = {"name": "New " + new_problem["type"] + " Case #" + str(len(case_base) + 1) + 
                        " (" + new_problem["area"] + ", " + str(new_problem["population"]) + ")",
                "problem": new_problem,
                "solution": new_solution}
    case_base.append(new_case)
    print("New disaster case saved!")

    print("")
    print("UPDATED CASE BASE:")
    number = 1
    for case in case_base:
        print(str(number) + ". " + case["name"])
        number = number + 1
    print("Total cases: " + str(len(case_base)))

    # continue or no?
    print("")
    again = input("Analyze another disaster? (y/n): ").strip().lower()
    if again == "n":
        print("Goodbye!")
        break