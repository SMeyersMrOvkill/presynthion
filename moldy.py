import random
import json
import random
import json
import xml.etree.ElementTree as ET

def generate_random_polygon():
    # Define the possible locations
    locations = ['Left', 'Right', 'Top', 'Bottom', 'TopLeft', 'TopRight', 'BottomLeft', 'BottomRight', 'Center']
    
    # Define the possible shapes
    shapes = ['Rectangle', 'Square', 'Circle', 'Triangle', 'Pentagon', 'Hexagon', 'Octagon', 'Star', 'Custom']
    
    # Generate a random location
    location = random.choice(locations)
    
    # Generate a random shape based on the probabilities
    shape_choice = random.choices(shapes, weights=[12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 6.75, 6.75, 12.5], k=1)[0]
    
    # Generate random coordinates based on the location
    if location == 'Left':
        x = random.randint(64, 128)
        y = random.randint(64, 512-64)
    elif location == 'Right':
        x = random.randint(384, 512-64)
        y = random.randint(64, 512-64)
    elif location == 'Top':
        x = random.randint(64, 512-64)
        y = random.randint(64, 128)
    elif location == 'Bottom':
        x = random.randint(64, 512-64)
        y = random.randint(384, 512-64)
    elif location == 'TopLeft':
        x = random.randint(64, 128)
        y = random.randint(64, 128)
    elif location == 'TopRight':
        x = random.randint(384, 512-64)
        y = random.randint(50, 128)
    elif location == 'BottomLeft':
        x = random.randint(50, 128)
        y = random.randint(384, 512-64)
    elif location == 'BottomRight':
        x = random.randint(384, 512-64)
        y = random.randint(384, 512-64)
    else:  # Center
        x = random.randint(128, 384)
        y = random.randint(128, 384)
    
    # Generate the polygon based on the chosen shape
     # Generate the polygon based on the chosen shape
    fill_choice = random.choice(['gradient', 'random', 'none'])
    if fill_choice == 'gradient':
        colors = [f'rgb({random.random()}, {random.random()}, {random.random()})' for _ in range(2)]
        gradient = ET.Element('linearGradient', {'id': 'grad', 'x1': '0%', 'y1': '0%', 'x2': '100%', 'y2': '100%'})
        for i, color in enumerate(colors):
            ET.SubElement(gradient, 'stop', {'offset': f'{i / (len(colors) - 1):.2f}', 'stop-color': color})
        fill = 'url(#grad)'
    elif fill_choice == 'random':
        fill_color = f'rgb({random.randrange(0,255)}, {random.randrange(0,255)}, {random.randrange(0,255)})'
        fill = fill_color
    else:
        fill = 'none'

    outline_choice = random.choice(['rainbow', 'random', 'black'])
    if outline_choice == 'rainbow':
        colors = [f'rgb({random.random()}, {random.random()}, {random.random()})' for _ in range(7)]
        stroke = f'rgb({random.randrange(0, 255)},{random.randrange(0, 255)}.{random.randrange(0, 255)}'
        stroke_width = '5'
        stroke_dasharray = '10,5'
        stroke_linecap = 'round'
        stroke_linejoin = 'round'
        stroke_opacity = '0.8'
    elif outline_choice == 'random':
        outline_color = f'rgb({random.random()}, {random.random()}, {random.random()})'
        stroke = outline_color
        stroke_width = '1'
        stroke_dasharray = 'none'
        stroke_linecap = 'butt'
        stroke_linejoin = 'miter'
        stroke_opacity = '1'
    else:
        stroke = random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
        stroke_width = '1'
        stroke_dasharray = 'none'
        stroke_linecap = 'butt'
        stroke_linejoin = 'miter'
        stroke_opacity = '1'

    attributes = {
        'fill': fill,
        'stroke': stroke,
        'stroke-width': stroke_width,
        'stroke-dasharray': stroke_dasharray,
        'stroke-linecap': stroke_linecap,
        'stroke-linejoin': stroke_linejoin,
        'stroke-opacity': stroke_opacity
    }

    if shape_choice == 'Rectangle':
        width = random.randint(50, 150)
        height = random.randint(50, 150)
        attributes.update({'x': str(x), 'y': str(y), 'width': str(width), 'height': str(height)})
        polygon = ET.Element('rect', attributes)
    elif shape_choice == 'Square':
        size = random.randint(50, 150)
        attributes.update({'x': str(x), 'y': str(y), 'width': str(size), 'height': str(size)})
        polygon = ET.Element('rect', attributes)
    elif shape_choice == 'Circle':
        radius = random.randint(25, 75)
        attributes.update({'cx': str(x), 'cy': str(y), 'r': str(radius)})
        polygon = ET.Element('circle', attributes)
    else:  # Random polygon
        num_points = random.randint(3, 8)
        points = []
        for _ in range(num_points):
            px = random.randint(x - 50, x + 50)
            py = random.randint(y - 50, y + 50)
            points.append(f'{px},{py}')
        attributes.update({'points': ' '.join(points)})
        polygon = ET.Element('polygon', attributes)

    # Create the SVG image and add the polygon
    svg = ET.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg', 'width': '512', 'height': '512'})
    if fill_choice == 'gradient':
        svg.append(gradient)
    svg.append(polygon)
    tree = ET.ElementTree(svg)

    # Create the JSON dictionary
    json_data = {
        'location': location,
        'shape': shape_choice,
        'coordinates': {
            'x': x,
            'y': y
        },
        'fill': fill_choice,
        'outline': outline_choice
    }

    return tree, json_data

# Generate the random polygon and save the SVG image and JSON file
import random
import json
import svgwrite
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtSvgWidgets import QGraphicsSvgItem, QSvgWidget
from PySide6.QtCore import QTimer, Qt

import json
import xml.etree.ElementTree as ET

def combine_svg_images(svg1_root, props1, svg2_root, props2):
    # Append the content of the second SVG to the first SVG
    for child in svg2_root:
        svg1_root.append(child)

    # Convert the modified SVG to a string
    combined_svg = ET.tostring(svg1_root, encoding='unicode')

    # Combine the properties
    combined_props = {**props1, **props2}
    f = open("tmp.svg", "w")
    f.write(combined_svg)
    f.flush()
    f.close()

    return ET.parse("tmp.svg"), combined_props

ds = open("random-shapes-tiny.jsonl", "w")

MAX_LENGTH = 1024*1000*1000*5

global rows
rows = 0

class SVGSlideshow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Polygon Slideshow")
        self.setGeometry(100, 100, 512, 512)

        layout = QVBoxLayout()
        self.svg_widget = QSvgWidget()
        layout.addWidget(self.svg_widget)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_polygon)
        self.timer.start(1)  # Update every 1ms

    def update_polygon(self):
        global rows
        svg_image, json_dict = generate_random_polygon()
        if ing := random.randrange(1, 16) > 4:
            for nm in range(ing):
                svg_img, props = generate_random_polygon()
                svg_image, json_dict = combine_svg_images(svg_image.getroot(), json_dict, svg_img.getroot(), props)
        with open('polygon_data.json', 'w') as json_file:
            json.dump(json_dict, json_file)
        svg_image.write("random_polygon.svg")

        self.svg_widget.load('random_polygon.svg')
        
        fn = open("random_polygon.svg", "r")

        ds.write(json.dumps({
            "svg": fn.read(),
            "props": json_dict
        }) + "\n")
        ds.flush()
        fn.close()
        rows += 1
        self.setWindowTitle(str(rows))

if __name__ == '__main__':
    app = QApplication([])
    slideshow = SVGSlideshow()
    slideshow.show()
    app.exec()