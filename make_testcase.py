from tkinter import *

root = Tk()

width = 10
height = 10
output_file = "my_test_case.txt"
cell_size = 40

canvas = Canvas(root, width=(width+1)*cell_size, height=(height+1)*cell_size)
canvas.pack()
for i in range(width):
	canvas.create_line((i + 1) * cell_size, cell_size, (i + 1) * cell_size, height * cell_size)
	canvas.create_text((i + 1) * cell_size, int(cell_size / 4), text=str(i))
for j in range(height):
	canvas.create_line(cell_size, (j + 1) * cell_size, width * cell_size, (j + 1) * cell_size)
	canvas.create_text(int(cell_size / 4), (j + 1) * cell_size, text=str(j))

circles = dict()
last_coordinate = tuple()

def new_circle(event):
	global canvas, circle, width, height, last_coordinate
	x_coor = round(event.x / cell_size) * cell_size
	y_coor = round(event.y / cell_size) * cell_size
	if x_coor >= 0 and x_coor <= (width * cell_size) and y_coor >= 0 and y_coor <= (height * cell_size):
		last_coordinate = (round(event.x / cell_size) - 1, round(event.y / cell_size) - 1)
		if last_coordinate in circles:
			del circles[last_coordinate]
			canvas.delete(last_coordinate)
		else:
			canvas.create_oval(x_coor - (cell_size / 4), y_coor - (cell_size / 4), x_coor + (cell_size / 4), y_coor + (cell_size / 4), fill="white", tags=last_coordinate)
			circles[last_coordinate] = 0

def set_number(event):
	global last_coordinate, circles, width, height
	if event.char.isdigit() and last_coordinate:
		circles[last_coordinate] = int(event.char)
		canvas.create_text((last_coordinate[0] + 1) * cell_size, (last_coordinate[1] + 1) * cell_size, text=event.char, tags=last_coordinate)
	if event.char == '\r':
		result = "{0} | {1} | [".format(width, height)
		for key in sorted(list(circles.keys()), key=lambda circle: (circle[1] * width) + circle[0]):
			result += str(key + (circles[key],)) + ", "
		result = result[:-2] + "]"
		f = open(output_file, 'w')
		f.write(result)
		f.close()


canvas.focus_set()
canvas.bind("<Button-1>", new_circle)
canvas.bind("<Key>", set_number)

root.mainloop()
