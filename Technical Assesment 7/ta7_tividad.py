# TA 7 - Laboratory Activity

import math
import matplotlib.pyplot as plt

# the data from the table: size, orbit, habitable, count
all_planets = [
    ["Big", "Near", "Yes", 20],
    ["Big", "Far", "Yes", 170],
    ["Small", "Near", "Yes", 139],
    ["Small", "Far", "Yes", 45],
    ["Big", "Near", "No", 130],
    ["Big", "Far", "No", 30],
    ["Small", "Near", "No", 11],
    ["Small", "Far", "No", 255],
]

# which spot in each row is Size and which is Orbit
column_numbers = {"Size": 0, "Orbit": 1}

def count_habitable(planet_rows):
    # count how many planets are habitable and how many are not
    habitable_count = 0
    not_habitable_count = 0
    for planet in planet_rows:
        if planet[2] == "Yes":
            habitable_count = habitable_count + planet[3]
        else:
            not_habitable_count = not_habitable_count + planet[3]
    return habitable_count, not_habitable_count

def get_entropy(habitable_count, not_habitable_count):
    # entropy formula: -p * log2(p) for each group
    total = habitable_count + not_habitable_count
    entropy = 0.0
    if habitable_count > 0:
        chance_habitable = habitable_count / total
        entropy = entropy - chance_habitable * math.log2(chance_habitable)
    if not_habitable_count > 0:
        chance_not_habitable = not_habitable_count / total
        entropy = entropy - chance_not_habitable * math.log2(chance_not_habitable)
    return entropy

def get_values(planet_rows, column_name):
    # get the different values in a column, like Big and Small
    column_number = column_numbers[column_name]
    different_values = []
    for planet in planet_rows:
        if planet[column_number] not in different_values:
            different_values.append(planet[column_number])
    return different_values

def get_rows_with_value(planet_rows, column_name, value):
    # keep only the rows where the column equals the value
    column_number = column_numbers[column_name]
    matching_rows = []
    for planet in planet_rows:
        if planet[column_number] == value:
            matching_rows.append(planet)
    return matching_rows

def get_information_gain(planet_rows, column_name):
    # gain = entropy before split minus entropy after split
    habitable_count, not_habitable_count = count_habitable(planet_rows)
    total = habitable_count + not_habitable_count
    entropy_before = get_entropy(habitable_count, not_habitable_count)

    entropy_after = 0.0
    for value in get_values(planet_rows, column_name):
        rows_for_value = get_rows_with_value(planet_rows, column_name, value)
        value_habitable, value_not_habitable = count_habitable(rows_for_value)
        value_total = value_habitable + value_not_habitable
        # bigger groups count more
        weight = value_total / total
        entropy_after = entropy_after + weight * get_entropy(value_habitable, value_not_habitable)

    return entropy_before - entropy_after

def build_tree(planet_rows, columns_left):
    habitable_count, not_habitable_count = count_habitable(planet_rows)

    # make a leaf if all planets are the same answer or no columns are left
    if habitable_count == 0 or not_habitable_count == 0 or len(columns_left) == 0:
        if habitable_count >= not_habitable_count:
            answer = "Yes"
        else:
            answer = "No"
        return {"is_leaf": True, "answer": answer,
                "habitable": habitable_count, "not_habitable": not_habitable_count}

    # find the column with the biggest information gain
    best_column = ""
    best_gain = -1.0
    for column_name in columns_left:
        gain = get_information_gain(planet_rows, column_name)
        print("Gain of " + column_name + " = " + str(round(gain, 4)))
        if gain > best_gain:
            best_gain = gain
            best_column = column_name
    print("Splitting on " + best_column)
    print("")

    # the chosen column can't be used again lower in the tree
    new_columns_left = []
    for column_name in columns_left:
        if column_name != best_column:
            new_columns_left.append(column_name)

    # make one branch for each value of the best column
    branches = {}
    for value in get_values(planet_rows, best_column):
        print("Branch: " + best_column + " = " + value)
        rows_for_value = get_rows_with_value(planet_rows, best_column, value)
        branches[value] = build_tree(rows_for_value, new_columns_left)

    return {"is_leaf": False, "column": best_column, "branches": branches}


def print_tree(node, spaces):
    if node["is_leaf"]:
        print(spaces + "Habitable = " + node["answer"] + " (" + str(node["habitable"])
              + " habitable, " + str(node["not_habitable"]) + " not habitable)")
    else:
        for value in node["branches"]:
            print(spaces + node["column"] + " = " + value)
            print_tree(node["branches"][value], spaces + "    ")


def predict(node, size, orbit):
    # go down the tree until we hit a leaf
    if node["is_leaf"]:
        return node["answer"]
    if node["column"] == "Size":
        next_node = node["branches"][size]
    else:
        next_node = node["branches"][orbit]
    return predict(next_node, size, orbit)


def draw_node(axes, node, depth, leaf_positions):
    # draws one node and returns its x and y position
    # y goes down by 2 for every level of the tree
    y_position = 0 - depth * 2

    if node["is_leaf"]:
        # leaves are placed left to right, 4 units apart
        x_position = len(leaf_positions) * 4
        leaf_positions.append(x_position)
        leaf_text = ("Habitable = " + node["answer"] + "\n("
                     + str(node["habitable"]) + " Yes / "
                     + str(node["not_habitable"]) + " No)")
        axes.text(x_position, y_position, leaf_text, ha="center", va="center",
                  fontsize=10, zorder=3,
                  bbox=dict(boxstyle="round", facecolor="lightgreen", edgecolor="black"))
        return x_position, y_position

    # not a leaf, so draw the children first to know where they are
    child_x_positions = []
    child_y_positions = []
    child_values = []
    for value in node["branches"]:
        child_x, child_y = draw_node(axes, node["branches"][value], depth + 1, leaf_positions)
        child_x_positions.append(child_x)
        child_y_positions.append(child_y)
        child_values.append(value)

    # put this node in the middle of its children
    total_x = 0
    for child_x in child_x_positions:
        total_x = total_x + child_x
    x_position = total_x / len(child_x_positions)

    # draw a line to each child and write the branch value on it
    for index in range(len(child_x_positions)):
        axes.plot([x_position, child_x_positions[index]],
                  [y_position, child_y_positions[index]], color="black", zorder=1)
        middle_x = (x_position + child_x_positions[index]) / 2
        middle_y = (y_position + child_y_positions[index]) / 2
        axes.text(middle_x, middle_y, child_values[index], ha="center", va="center",
                  fontsize=10, zorder=2,
                  bbox=dict(boxstyle="round", facecolor="white", edgecolor="none"))

    # draw the box for this node (the column it splits on)
    axes.text(x_position, y_position, node["column"], ha="center", va="center",
              fontsize=12, fontweight="bold", zorder=3,
              bbox=dict(boxstyle="round", facecolor="lightblue", edgecolor="black"))
    return x_position, y_position


def draw_tree(tree):
    figure, axes = plt.subplots(figsize=(10, 6))
    leaf_positions = []
    draw_node(axes, tree, 0, leaf_positions)
    axes.set_title("ID3 Decision Tree: Is the Planet Habitable?")
    axes.set_xlim(-2, 14)
    axes.set_ylim(-5, 1)
    axes.axis("off")
    plt.savefig("decision_tree.png", dpi=150, bbox_inches="tight")
    plt.show()

# main part
decision_tree = build_tree(all_planets, ["Size", "Orbit"])
print("")
print("FINAL TREE")
print_tree(decision_tree, "")
print("")
print("a. Big and Far: " + predict(decision_tree, "Big", "Far"))
print("b. Small and Near: " + predict(decision_tree, "Small", "Near"))
# draw the tree and save it as decision_tree.png
draw_tree(decision_tree)