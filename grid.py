class Island:
	def __init__(self, x, y, capacity):
		"""
		Takes in x value, y value, and initial bridge capacity.
		Each island knows its location, current capacity, neighbors, and bridges connected (also a visited flag for DFS).
		"""
		self.x = x
		self.y = y
		self.capacity = capacity
		self.neighbors = list()
		self.bridges = list()
		self.visited = False

	@property
	def neighbor_num(self):
		"""
		Returns number of neighbors adjacent to self.
		"""
		#Count items in self.neighbors that are not None
		return len(list(filter(lambda x: x, self.neighbors.values())))
	@property 
	def bridge_num(self):
		"""
		Returns number of bridges currently connected to self.
		"""
		return len(self.bridges)

	@property
	def complete(self):
		"""
		Returns True of self is fully connected (capacity is 0), and False otherwise.
		"""
		return self.capacity == 0

	def add_neighbor(self, island):
		"""
		Adds neighbor to self. Symmetry not enforced--self must be added as neighbor manually.
		"""
		self.neighbors.append(island)

	def bridges_to(self, neighbor):
		"""
		Returns number of bridges currently made with a neighbor; either 0, 1, or 2.
		"""
		#Count number of bridges already made with neighbor
		b = Bridge(self, neighbor)
		return self.bridges.count(b)

	def add_bridge(self, bridge):
		"""
		Adds bridge to self, decrements capacity.
		"""
		self.bridges.append(bridge)
		self.capacity -= 1

	def delete_bridge(self, bridge):
		"""
		Deletes bridge, increments capacity.
		"""
		self.bridges.remove(bridge)
		self.capacity += 1

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (self.x == other.x) and (self.y == other.y)
		else:
			return False

	def __str__(self):
		return str(self.capacity)

	def __repr__(self):
		return "({0},{1})_{2}".format(self.x, self.y, self.capacity)


class Bridge:

	def __init__(self, island1, island2):
		"""
		Takes in two Islands. Calculates orientation: 1 if vertical, -1 if horizontal.
		Enforces that island1 has smaller x than island2 if horizontal, and island1
		has smaller y than island2 if vertical.
		"""
		self.orientation = 1 if (island1.x == island2.x) else -1
		#orientation = 1 if vertical, -1 if horizontal
		if self.orientation == 1:
			if island1.y < island2.y:
				self.island1, self.island2 = island1, island2
			else:
				self.island1, self.island2 = island2, island1
		else:
			if island1.x < island2.x:
				self.island1, self.island2 = island1, island2
			else:
				self.island1, self.island2 = island2, island1

	def intersects(self, other):
		"""
		Returns true if self intersects with other bridge. 
		"""
		if other.orientation == self.orientation: #Cannot intersect if parallel
			return False
		if self.orientation == 1: #self is vertical, so other is horizontal
			return (other.island1.y > self.island1.y) and (other.island1.y < self.island2.y) and (self.island1.x > other.island1.x) and (self.island1.x < other.island2.x)
		else: #self is horizontal, so other is vertical
			return (self.island1.y > other.island1.y) and (self.island1.y < other.island2.y) and (other.island1.x > self.island1.x) and (other.island1.x < self.island2.x)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (self.island1 == other.island1) and (self.island2 == other.island2)
		else:
			return False

	def __repr__(self):
		return "({0},{1})--({2},{3})".format(self.island1.x, self.island1.y, self.island2.x, self.island2.y)

class IslandList:

	def __init__(self):
		"""
		Wrapper class for list of islands.
		"""
		self.island_list = list()
		self.island_dict = dict()

	def add_island(self, island):
		"""
		Adds island to island_list and island_dict (for fast lookup).
		"""
		self.island_list.append(island)
		self.island_dict[(island.x, island.y)] = island

	def get_island(self, x, y):
		"""
		Retrieves island at given (x, y) coordinate if it exists; returns None otherwise.
		"""
		if (x,y) in self.island_dict:
			return self.island_dict[(x, y)]
		return None

	def set_all_unvisited(self):
		"""
		Sets visited flag of all islands to False for DFS.
		"""
		for island in self.island_list:
			island.visited = False

	def exists_unvisited(self):
		"""
		Returns True if there exists an island in island_list that has a visited flag set to False (unvisited),
		returns False if all islands have been visited (all flags set to True).
		"""
		for island in self.island_list:
			if not island.visited:
				return True
		return False

	def all_complete(self):
		"""
		Returns True if all islands are complete (capacities are 0), returns False otherwise.
		"""
		for island in self.island_list:
			if not island.complete:
				return False
		return True

	def __repr__(self):
		return repr(self.island_list)

class BridgeList:

	def __init__(self):
		"""
		Wrapper class for list of bridges.
		"""
		self.bridge_list = list()

	def add_bridge(self, bridge):
		"""
		Adds bridge to bridge_list.
		"""
		self.bridge_list.append(bridge)

	def delete_bridge(self, bridge):
		"""
		Deletes bridge from bridge_list.
		"""
		self.bridge_list.remove(bridge)

	def conflict(self, potential_bridge):
		"""
		Given a potential bridge, returns True if it will intersect any existing bridge
		in bridge_list, returns False otherwise.
		"""
		for bridge in self.bridge_list:
			if bridge.intersects(potential_bridge):
				return True
		return False

	def __repr__(self):
		return repr(self.bridge_list)

class Grid:

	def __init__(self, width, height):
		"""
		Takes in width and height of grid. A Grid knows its dimensions, list of islands, 
		and list of bridges.
		"""
		self.width = width;
		self.height = height;
		self.islands = IslandList()
		self.bridges = BridgeList()

	def add_island(self, x, y, capacity):
		"""
		Adds island to list of islands given coordinate and capacity.
		"""
		island = Island(x, y, capacity)
		self.islands.add_island(island)

	def update_neighbors(self):
		"""
		Finds existing adjacent neighbors for each island and connects them.
		"""
		for island in self.islands.island_list:
			x = island.x
			y = island.y
			#West:
			i = x - 1
			while i >= 0:
				neighbor = self.islands.get_island(i, y)
				if neighbor:
					if neighbor not in island.neighbors:
						island.add_neighbor(neighbor)
					if island not in neighbor.neighbors:
						neighbor.add_neighbor(island)
					break
				i -= 1
			#East:
			i = x + 1
			while i < self.width:
				neighbor = self.islands.get_island(i, y)
				if neighbor:
					if neighbor not in island.neighbors:
						island.add_neighbor(neighbor)
					if island not in neighbor.neighbors:
						neighbor.add_neighbor(island)
					break
				i += 1
			#North:
			j = y - 1
			while j >= 0:
				neighbor = self.islands.get_island(x, j)
				if neighbor:
					if neighbor not in island.neighbors:
						island.add_neighbor(neighbor)
					if island not in neighbor.neighbors:
						neighbor.add_neighbor(island)
					break
				j -= 1
			#South:
			j = y + 1
			while j < self.height:
				neighbor = self.islands.get_island(x, j)
				if neighbor:
					if neighbor not in island.neighbors:
						island.add_neighbor(neighbor)
					if island not in neighbor.neighbors:
						neighbor.add_neighbor(island)
					break
				j += 1

	def add_bridge(self, bridge):
		"""
		Adds bridge to list of bridges. Adds bridge to each participating island.
		"""
		self.bridges.add_bridge(bridge)
		bridge.island1.add_bridge(bridge)
		bridge.island2.add_bridge(bridge)

	def delete_bridge(self, bridge):
		"""
		Deletes bridge from list of bridges. Deletes bridge from each participating island.
		"""
		self.bridges.delete_bridge(bridge)
		bridge.island1.delete_bridge(bridge)
		bridge.island2.delete_bridge(bridge)

	def valid_bridges(self):
		"""
		Calculates valid bridges. Checks every island's every neighbor. A bridge is valid
		if it will not conflict with any existing bridge. Valid bridges may conflict with each
		other. Each pair of islands can only have one valid bridge--double bridges not included.
		"""
		v_bridges = list()
		for island in self.islands.island_list:
			if island.complete:
				continue
			for neighbor in island.neighbors:
				if not neighbor.complete and island.bridges_to(neighbor) < 2:
					potential_bridge = Bridge(island, neighbor)
					if not self.bridges.conflict(potential_bridge) and potential_bridge not in v_bridges:
					# Make sure will not conflict existing bridges
						v_bridges.append(potential_bridge)
		return v_bridges 

	def dfs(self, island):
		"""
		Conducts depth-first search on list if islands. Starts with given island and
		visits neighbors only if connected by a bridge. Used to check if islands are
		well-connected.
		"""
		island.visited = True
		for bridge in island.bridges:
			if bridge.island1 == island: #Call dfs on connected island
				connected_neighbor = bridge.island2
			else:
				connected_neighbor = bridge.island1
			if not connected_neighbor.visited:
				x = self.dfs(connected_neighbor)

	def status_helper(self):
		"""
		Helper function to check status of grid. Checks each individual island. If an island has
		a larger capacity than available connections, the grid is incorrect. If an island has a
		smaller capacity than available connections, the grid is incomplete. Incorrect trumps 
		incomplete. Returns -1 if incorrect, 0 if incomplete, 1 if potentially complete.
		"""
		bridge_sets = {}
		for bridge in self.bridges.bridge_list:
			b = (bridge.island1.x, bridge.island1.y, bridge.island2.x, bridge.island2.y)
			bridge_sets[b] = bridge_sets.get(b, 0) + 1
		for counts in bridge_sets.values():
			if counts > 2:
				return -1
		for island in self.islands.island_list:
			potential_bridge_num = 0
			for neighbor in island.neighbors:
				if not self.bridges.conflict(Bridge(island, neighbor)):
					potential_bridge_num += neighbor.capacity
			if potential_bridge_num < island.capacity or island.capacity < 0:
				return -1 #Incorrect (need more bridges than can be made)
			if island.capacity != 0:
				return 0 #Incomplete
		return 1

	def status(self):
		"""
		Calculates status of grid. Calls status_helper and dfs. If status_helper determines
		that grid is incorrect or incomplete, then status returns same result. If status_helper
		determines that grid is potentially complete, then call dfs and check that islands
		are well-connected. If well-connected, grid is complete, return 1. Returns 0 if incomplete
		and -1 if incorrect.
		"""
		x = self.status_helper()
		if x == 1:
			self.islands.set_all_unvisited()
			self.dfs(self.islands.island_list[0])
			if self.islands.exists_unvisited(): #Incorrect (not well-connected)
				return -1
		return x

	def __repr__(self):
		return "Islands: " + repr(self.islands) + "\n" + "Bridges: " + repr(self.bridges)

	def __str__(self):
		grid = [[" " for i in range(self.height)] for j in range(self.width)] #Index in width first, (0,0) is top left
		for island in self.islands.island_list:
			grid[island.x][island.y] = str(island.capacity)
		for bridge in self.bridges.bridge_list:
			if bridge.orientation == 1: #Vertical
				if grid[bridge.island1.x][bridge.island1.y + 1] == " ":
					char = "|"
				elif grid[bridge.island1.x][bridge.island1.y + 1] == "|":
					char = "#"
				else:
					char = "X"
				for i in range(bridge.island1.y + 1, bridge.island2.y):
					grid[bridge.island1.x][i] = char
			else:
				if grid[bridge.island1.x + 1][bridge.island1.y] == " ":
					char = "-"
				elif grid[bridge.island1.x + 1][bridge.island1.y] == "-":
					char = "#"
				else:
					char = "X"
				for i in range(bridge.island1.x + 1, bridge.island2.x):
					grid[i][bridge.island1.y] = char
		result = ""
		for i in range(len(grid[0])):
			result += " ".join([col[i] for col in grid]) + "\n"
		return result

