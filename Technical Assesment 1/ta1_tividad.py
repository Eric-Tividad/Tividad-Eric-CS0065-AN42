import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import Counter

animations = []  

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def setup(self):
        self.path = [] # stores positions of the dots

    def step(self):
        p = self.model.p
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)] # dot movement

        # for task 2: add more movement to the right
        if p.biased:
            dirs += [(1, 0)] * 3
        random.shuffle(dirs)

        # gets dots current spot, and tracks which location has been taken
        x, y = self.position
        taken = {a.position for a in self.model.agents if a is not self}

        for dx, dy in dirs:
            nx = max(0, min(p.grid_size[0] - 1, x + dx))
            ny = max(0, min(p.grid_size[1] - 1, y + dy))
            
            # skip cells if occupied
            if p.avoid and (nx, ny) in taken:
                continue
            self.position = (nx, ny)
            break
        self.path.append(self.position)

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        # i create ze agents
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        # put agents on random starting location
        for agent in self.agents:
            agent.position = (random.randint(0, self.p.grid_size[0]-1),
                              random.randint(0, self.p.grid_size[1]-1))
            agent.path.append(agent.position) # starting point
    
    # let agents gets their own turn
    def step(self):
        for agent in self.agents:
            agent.step()

def run(agents, size, steps, avoid=False, biased=False, label="Run"):
    params = {'agents': agents, 
              'grid_size': (size, size), 
              'steps': steps,
              'avoid': avoid, 
              'biased': biased}
    
    model = RandomWalkModel(params)
    model.setup()
    
    for _ in range(steps):
        model.step()

    # for task 3: collects final position
    print(label)
    print(f"Agents={agents}, Grid={size}x{size}, Steps={steps}, avoid={avoid}, biased={biased}")
    finals = [a.position for a in model.agents]
    for i, pos in enumerate(finals, 1):
        print(f"  Agent {i}: final position = {pos}")
    avg_x = sum(p[0] for p in finals) / len(finals)
    avg_y = sum(p[1] for p in finals) / len(finals)
    print(f"  Average final position: ({avg_x:.2f}, {avg_y:.2f})")
    print(f"  Cells with 2+ agents: {sum(1 for c in Counter(finals).values() if c > 1)}")

    # for task 1: plotting paths
    fig, ax = plt.subplots()
    for i, a in enumerate(model.agents, 1):
        xs = [p[0] for p in a.path]; ys = [p[1] for p in a.path]
        ax.plot(xs, ys, marker='.', alpha=0.6, label=f"Agent {i}")
        ax.scatter(xs[0], ys[0], marker='s', s=60)     # start
        ax.scatter(xs[-1], ys[-1], marker='*', s=150)  # end

    ax.set_xlim(-0.5, size - 0.5); ax.set_ylim(-0.5, size - 0.5)

    ax.set_xticks(range(size)); ax.set_yticks(range(size)); ax.grid(True)

    ax.set_title(f"{label}: paths (square=start, star=end)")

    if agents <= 10: 
        ax.legend(fontsize=7)

    # -------- Animation -----------
    # replays the saved paths of the agents, one step per frame
    fig2, ax2 = plt.subplots()
    ax2.set_xlim(-0.5, size - 0.5); ax2.set_ylim(-0.5, size - 0.5)
    ax2.set_xticks(range(size)); ax2.set_yticks(range(size)); ax2.grid(True)
    scat = ax2.scatter([], [], s=200) # s = size of agents

    def update(frame):
        # frame 0 = starting positions, frame 1 = after step 1, and so on
        x = [a.path[frame][0] for a in model.agents]
        y = [a.path[frame][1] for a in model.agents]
        scat.set_offsets(list(zip(x, y)))
        ax2.set_title(f"{label}: step {frame}/{steps}")
        return scat,

    ani = animation.FuncAnimation(fig2, update, frames=steps + 1,
                                  blit=False, repeat=False)
    animations.append(ani) # keep a reference so the animation doesn't get deleted

    return finals

print("Technical Assesment 1: Random Walk Simulation Using AgentPY")
print("1 - Scenario A (5 agents, 10x10 grid, 20 steps, plain random walk)")
print("2 - Scenario B (20 agents, 10x10 grid, 50 steps, avoid + preferred direction)")
print("3 - Enter my own values")
choice = input("Pick a mode: ").strip()
 
if choice == "1":
    run(5, 10, 20, label="Scenario A")
elif choice == "2":
    run(20, 10, 50, avoid=True, biased=True, label="Scenario B")
elif choice == "3":
    n_agents = int(input("Number of agents: "))
    grid = int(input("Grid size (e.g., 10 for 10x10): "))
    n_steps = int(input("Number of steps: "))
    run(n_agents, grid, n_steps, label="Custom Run")
else:
    print("Invalid choice. Please run again and enter 1, 2, or 3.")
    exit()
 
plt.show()