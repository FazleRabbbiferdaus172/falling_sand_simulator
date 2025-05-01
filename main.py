import pygame
import random
import asyncio

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Falling Sand Simulation")
clock = pygame.time.Clock()
running = True
dt = 0
grid_size = 600
pxl_size = 1
dune_grid = [[0 for _ in range(grid_size//pxl_size)] for _ in range(grid_size//pxl_size)]
len_dune_grid = len(dune_grid)
move_offset_mapper = {
	"nowhere": (0,0),
	"bottom": (0,1),
	"bottom_left": (-1,1),
	"bottom_right": (1,1)
}
sands = []

def color_generator():
	color = [random.randint(1, 100) for _ in range(3)]
	index = 0
	while True:
		offset = random.randint(0,1 )
		color[index] = color[index] + offset
		if color[index] > 254:
			index = (index + 1) % 3
		if index == 0 and color[2] > 254:
			color = [random.randint(1, 100) for _ in range(3)]
		yield color[0], color[1], color[2]

color_gen = color_generator()



class Sand:
	def __init__(self, x, y):
		self.x = x // pxl_size
		self.y = y // pxl_size
		self.color = next(color_gen)
		self.sand_obj = None

	def draw(self):
		self.sand_obj = pygame.draw.rect(
			screen, self.color, (self.x * pxl_size, self.y * pxl_size, pxl_size, pxl_size)
		)
		self.update_dune_grid(1)

	def move(self):
		move_to = self.can_move_to()
		if move_to == "nowhere":
			return
		x_offset, y_offset = move_offset_mapper[move_to]
		self.update_dune_grid(0)
		self.x += x_offset
		self.y += y_offset
		self.update_dune_grid(1)

	def can_move_to(self):
		result = "nowhere"
		# print(self.x, self.y)
		if self.y == len_dune_grid - 1:
			result = "nowhere"
		elif self.x == 0:
			result = "nowhere"
		elif self.x == len_dune_grid - 1:
			result = "nowhere"
		elif dune_grid[self.x][self.y + 1] == 0:
			result = "bottom"
		elif dune_grid[self.x][self.y + 1] == 1:
			if dune_grid[self.x + 1][self.y + 1] == 0 and dune_grid[self.x - 1][self.y + 1] == 0:
				choice = random.randint(0, 1)
				result = "bottom_left" if choice == 0 else "bottom_right"
			elif dune_grid[self.x - 1][self.y + 1] == 0 and dune_grid[self.x + 1][self.y + 1] == 1:
				result = "bottom_left"
			elif dune_grid[self.x + 1][self.y + 1] == 0 and dune_grid[self.x - 1][self.y + 1] == 1:
				result = "bottom_right"
		return result

	def update_dune_grid(self, val):
		dune_grid[self.x][self.y] = val

async def main():
	global running
	while running:
		await asyncio.sleep(0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		m_x, m_y = pygame.mouse.get_pos()
		amount = random.randint(0, 2)
		for _ in range(amount):
			rand_x = (m_x + random.randrange(-10, 10)) % grid_size
			rand_y = (m_y + random.randrange(-20, 10)) % grid_size
			sands.append(Sand(rand_x, rand_y))
		screen.fill("black")
		for sand in sands:
			sand.move()
			sand.draw()
		pygame.display.update()
		clock.tick(60)


asyncio.run(main())
