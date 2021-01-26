from grid import *

class Solver:

	def __init__(self, width, height, island_list):
		#Islands are 3-tuples (x, y, capacity)
		self.width = width
		self.height = height
		self.grid = Grid(width, height)
		for island in island_list:
			self.grid.add_island(island[0], island[1], island[2])
		self.grid.update_neighbors()
		self.island_list = island_list[:] # Untouched copy
		self.bridge_list = list()

	def search(self): # Mutates self.grid, returns 1 if solved, -1 if failed to solve
		status = self.grid.status()
		if status == 1:
			return 1
		if status == -1:
			return -1
		# If number of bridges needed same as number of valid bridges, logic_bridges adds all
		logic_bridges = self.logic()
		last_logic_round = logic_bridges[:] #Copy of logic_bridges initially
		while(last_logic_round): #Continuously run logic until no more logical moves
			last_logic_round = self.logic()
			logic_bridges.extend(last_logic_round)
		if self.grid.status() == 1:
			return 1 # Complete
		v_bridges = self.grid.valid_bridges() # Incomplete, try bridges
		for bridge in v_bridges:
			self.grid.add_bridge(bridge)
			result = self.search()
			if result == -1:
				self.grid.delete_bridge(bridge)
			if result == 1:
				return 1
		# At this point, no valid bridges result in solution, so undo logic bridges and return -1 
		# (backtrack, so previous call can delete offending bridge and try another one)
		for bridge in logic_bridges:
			self.grid.delete_bridge(bridge)
		return -1

	def logic(self): # Mutates self.grid, returns list of bridges that it makes
		"""
		Logical Algorithm
		1. If island capacity equals available bridge connections, connect all bridges and island is done
		2. If islandNum > 2*(available directions - 1), connect single bridge in all available directions
		3. Let newIslandNum be islandNum after subtracting the number of directions where only a single bridge can be built. 
		 	If newIslandNum > 2*(available directions (not including single restrictions) - 1), connect single bridge in all unrestricted directions
		"""
		logic_bridges = list()
		for island in self.grid.islands.island_list:
			v_bridges = self.grid.valid_bridges()
			potential_bridges = list(filter(lambda bridge: (bridge.island1 == island) or (bridge.island2 == island), v_bridges)) # Bridges that involve island
			available_directions = len(potential_bridges) # Number of possible directions
			available_connections = 0
			singly_restricted_temp_bridges = list() # Bridges that cannot be made twice
			temp_bridges = list()
			for neighbor in island.neighbors:
				b = Bridge(neighbor, island)
				if b in potential_bridges:
					if neighbor.capacity == 1:
						available_connections += 1
						temp_bridges.append(b)
						singly_restricted_temp_bridges.append(b)
					elif neighbor.capacity >= 2:
						available_connections += 2
						temp_bridges.append(b)
						temp_bridges.append(b)
			if available_connections == island.capacity:
				for bridge in temp_bridges:
					self.grid.add_bridge(bridge)
					logic_bridges.append(bridge)
			elif island.capacity > (2 * (available_directions - 1)):
				for bridge in potential_bridges:
					self.grid.add_bridge(bridge)
					logic_bridges.append(bridge)
			elif (island.capacity - len(singly_restricted_temp_bridges)) > (2 * (available_directions - len(singly_restricted_temp_bridges) - 1)):
				for bridge in potential_bridges:
					if bridge not in singly_restricted_temp_bridges:
						self.grid.add_bridge(bridge)
						logic_bridges.append(bridge)
		return logic_bridges

	def __str__(self):
		grid = [[" " for i in range(self.height)] for j in range(self.width)] # Index in width first, (0,0) is top left
		for island in self.island_list:
			grid[island[0]][island[1]] = str(island[2])
		for bridge in self.grid.bridges.bridge_list:
			if bridge.orientation == 1: # Vertical
				if grid[bridge.island1.x][bridge.island1.y + 1] == " ":
					char = "|"
				else:
					char = "#"
				for i in range(bridge.island1.y + 1, bridge.island2.y):
					grid[bridge.island1.x][i] = char
			else:
				if grid[bridge.island1.x + 1][bridge.island1.y] == " ":
					char = "-"
				else:
					char = "#"
				for i in range(bridge.island1.x + 1, bridge.island2.x):
					grid[i][bridge.island1.y] = char
		result = ""
		for i in range(len(grid[0])):
			result += " ".join([col[i] for col in grid]) + "\n"
		return result
