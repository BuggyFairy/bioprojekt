from bokeh.plotting import figure, output_file, show
from tile import Tile

def get_x_coordinates(list):
    return [x[0] for x in list]

def get_y_coordinates(list):
    return [x[1] for x in list]

def shift_coordinates(list, x_offset, y_offset):
    for i in range(0, len(list)):
        x = list[i][0]
        y = list[i][1]
        list[i] = (x + x_offset, y + y_offset)

def rotate_figure(list):
    figure = list[:]
    for i in range(0,3):
        for j in range(0, len(list)):
            x = list[j][0]
            y = list[j][1]
            list[j] = (y, -x)
        figure.extend(list)
    return figure


width_lines = 1.5
font_size = '9pt'

an_coordinates = [(0, y) for y in range(12, -1, -1)] + [(2, y) for y in range(0, 13)]
ae_coordinates = [(x, 0) for x in range(17, -1, -1)] + [(x, 2) for x in range(0, 18)]
as_coordinates = [(0, y) for y in range(-17, 1)] + [(2, y) for y in range(0, -18, -1)]
aw_coordinates = [(x, 0) for x in range(-12, 1)] + [(x, 2) for x in range(0, -13, -1)]

c_side = [(1, y) for y in range(13, 1, -1)] + [(x, 1) for x in range(2, 14)]
c_coordinates = rotate_figure(c_side)

shift_coordinates(an_coordinates, 49, 70)
shift_coordinates(ae_coordinates, 70, 49)
shift_coordinates(as_coordinates, 49, 30)
shift_coordinates(aw_coordinates, 30, 49)
shift_coordinates(c_coordinates, 50, 50)

plot = figure(plot_width=800, plot_height=800, x_range=(0,100), y_range=(0,100))

plot.line(x=get_x_coordinates(an_coordinates), y=get_y_coordinates(an_coordinates), line_width = width_lines, color='#00ff00')
plot.line(x=get_x_coordinates(ae_coordinates), y=get_y_coordinates(ae_coordinates), line_width = width_lines, color='#ff00ff')
plot.line(x=get_x_coordinates(as_coordinates), y=get_y_coordinates(as_coordinates), line_width = width_lines, color='#ffcc00')
plot.line(x=get_x_coordinates(aw_coordinates), y=get_y_coordinates(aw_coordinates), line_width = width_lines, color='#262626')
plot.line(x=get_x_coordinates(c_coordinates), y=get_y_coordinates(c_coordinates), line_width = width_lines, color='#cc0000')

tile = Tile.from_file("..\Examples\TileA2.fasta")

plot.text(x=get_x_coordinates(an_coordinates), y=get_y_coordinates(an_coordinates), text=tile.n, text_font_size=font_size)
plot.text(x=get_x_coordinates(ae_coordinates), y=get_y_coordinates(ae_coordinates), text=tile.e, text_font_size=font_size)
plot.text(x=get_x_coordinates(as_coordinates), y=get_y_coordinates(as_coordinates), text=tile.s, text_font_size=font_size)
plot.text(x=get_x_coordinates(aw_coordinates), y=get_y_coordinates(aw_coordinates), text=tile.w, text_font_size=font_size)

output_file("line.html")
show(plot)
