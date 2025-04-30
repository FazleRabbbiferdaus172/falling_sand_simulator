import pygame

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True
dt = 0

dune_grid = [[0 for _ in range(600)] for _ in range(600)]

def draw_sand(x: int,y: int, color: str):
	pygame.draw.circle(
		screen, color, (x, y), 1
	)
	pygame.display.flip()

def draw_dune():
	for i in range(600):
		for j in range(600):
			if dune_grid[i][j] == 1:
				draw_sand(i, j)

def update_sand_position():
	for i in range(600):
		for j in range(599):
			if dune_grid[i][j] == 1:
				draw_sand(i,j-1, "black")
				draw_sand(i,j, "red")
				if dune_grid[i][j+1] == 0:
					dune_grid[i][j+1] = 1
					dune_grid[i][j] = 0
			#elif dune_grid[i][j] == 0:
			#	draw_sand(i, j, "black")

def main():
	global running
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				m_x, m_y = pygame.mouse.get_pos()
				dune_grid[m_x][m_y] = 1

		#screen.fill("purple")
		update_sand_position()
		#pygame.display.flip()
		dt = clock.tick(60) / 100

if __name__ == "__main__":
	main()
