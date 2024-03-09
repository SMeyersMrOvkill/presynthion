import random
import math
import xml.etree.ElementTree as ET

class RandomFaceMath:
    def __init__(self):
        self.eye_functions = {
            'human': self._generate_human_eyes,
            'cyclops': self._generate_cyclops_eye,
            'triclops': self._generate_triclops_eyes
        }
        self.mouth_functions = {
            'happy': self._generate_happy_mouth,
            'sad': self._generate_sad_mouth,
            'neutral': self._generate_neutral_mouth
        }
        self.parameters = {}

    def generate_random_color(self):
        """Generates a bright, random RGB color."""
        r = random.randint(128, 255)
        g = random.randint(128, 255)
        b = random.randint(128, 255)
        color = f"rgb({r}, {g}, {b})"
        self.parameters['color_r'] = r
        self.parameters['color_g'] = g
        self.parameters['color_b'] = b
        return color

    def generate_face_outline(self, center_x, center_y, radius_x, radius_y):
        """Generates the face outline as an oval polygon."""
        num_points = random.randint(5, 10)
        points = " ".join([f"{center_x + radius_x * math.cos(2 * math.pi * i / num_points)}, {center_y + radius_y * math.sin(2 * math.pi * i / num_points)}" for i in range(num_points)])
        face_color = self.generate_random_color()
        self.parameters['center_x'] = center_x
        self.parameters['center_y'] = center_y
        self.parameters['radius_x'] = radius_x
        self.parameters['radius_y'] = radius_y
        self.parameters['num_points'] = num_points
        self.parameters['face_color'] = face_color
        return f'<polygon points="{points}" fill="{face_color}" stroke="black" stroke-width="2.5"/>'

    def generate_eyes(self, eye_type, center_x, center_y, radius_x, radius_y):
        """Generates the eyes based on the selected eye type."""
        generate_eye_func = self.eye_functions.get(eye_type, lambda *args: [])
        self.parameters['eye_type'] = eye_type
        return generate_eye_func(center_x, center_y, radius_x, radius_y)

    def _generate_human_eyes(self, center_x, center_y, radius_x, radius_y):
        eye_radius = random.randint(10, 20)
        eye_color = self.generate_random_color()
        left_eye_cx = center_x - radius_x // 3
        right_eye_cx = center_x + radius_x // 3
        eye_cy = center_y - radius_y // 3
        self.parameters['eye_radius'] = eye_radius
        self.parameters['eye_color'] = eye_color
        self.parameters['left_eye_cx'] = left_eye_cx
        self.parameters['right_eye_cx'] = right_eye_cx
        self.parameters['eye_cy'] = eye_cy
        return [
            f'<circle cx="{left_eye_cx}" cy="{eye_cy}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2" /><circle cx="{left_eye_cx}" cy="{eye_cy}" r="{eye_radius*int(random.randrange(4, 7)*0.10)}" fill="black" stroke="navy" stroke-width="2" z-index="2"/>',
            f'<circle cx="{right_eye_cx}" cy="{eye_cy}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2" /><circle cx="{right_eye_cx}" cy="{eye_cy}" r="{eye_radius*int(random.randrange(4, 7)*0.10)}" fill="black" stroke="navy" stroke-width="2" z-index="2"/>'
        ]

    def _generate_cyclops_eye(self, center_x, center_y, radius_x, radius_y):
        eye_radius = random.randint(20, 30)
        eye_color = self.generate_random_color()
        eye_cx = center_x
        eye_cy = center_y - radius_y // 3
        self.parameters['eye_radius'] = eye_radius
        self.parameters['eye_color'] = eye_color
        self.parameters['eye_cx'] = eye_cx
        self.parameters['eye_cy'] = eye_cy
        return [
            f'<circle cx="{eye_cx}" cy="{eye_cy}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2"/><circle cx="{eye_cx}" cy="{eye_cy}" r="5" fill="black" stroke="navy" stroke-width="2"/>'
        ]

    def _generate_triclops_eyes(self, center_x, center_y, radius_x, radius_y):
        eye_radius = random.randint(10, 15)
        eye_color = self.generate_random_color()
        eye_cx = center_x
        eye_cy = center_y - radius_y // 3
        left_eye_cx = eye_cx - radius_x // 4
        right_eye_cx = eye_cx + radius_x // 4
        self.parameters['eye_radius'] = eye_radius
        self.parameters['eye_color'] = eye_color
        self.parameters['eye_cx'] = eye_cx
        self.parameters['eye_cy'] = eye_cy
        self.parameters['left_eye_cx'] = left_eye_cx
        self.parameters['right_eye_cx'] = right_eye_cx
        return [
            f'<circle cx="{left_eye_cx}" cy="{eye_cy}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2"/><circle cx="{left_eye_cx}" cy="{eye_cy}" r="{eye_radius*int(random.randrange(4, 7)*0.10)}" fill="black" stroke="navy" stroke-width="2"/>',
            f'<circle cx="{eye_cx}" cy="{eye_cy - radius_y // 6}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2"/><circle cx="{eye_cx}" cy="{eye_cy - radius_y // 6}" r="{eye_radius*int(random.randrange(4, 7)*0.10)}" fill="black" stroke="navy" stroke-width="2"/>',
            f'<circle cx="{right_eye_cx}" cy="{eye_cy}" r="{eye_radius}" fill="{eye_color}" stroke="black" stroke-width="2"/><circle cx="{right_eye_cx}" cy="{eye_cy}" r="{eye_radius*int(random.randrange(4, 7)*0.10)}" fill="black" stroke="navy" stroke-width="2"/>'
        ]

    def generate_nose(self, center_x, center_y, radius_x, radius_y):
        """Generates the nose as a polygon."""
        nose_y_range = radius_y // 4
        nose_points = " ".join([
            f"{center_x}", f"{center_y + random.randint(-nose_y_range, nose_y_range)}",
            f"{center_x - radius_x // 5}", f"{center_y + radius_y // 2}",
            f"{center_x + radius_x // 5}", f"{center_y + radius_y // 2}"
        ])
        nose_color = self.generate_random_color()
        self.parameters['nose_points'] = nose_points
        self.parameters['nose_color'] = nose_color
        return f'<polygon points="{nose_points}" fill="{nose_color}" stroke="black" stroke-width="2"/>'

    def generate_mouth(self, mouth_type, center_x, center_y, radius_x, radius_y):
        """Generates the mouth based on the selected mouth type."""
        generate_mouth_func = self.mouth_functions.get(mouth_type, lambda *args: "")
        self.parameters['mouth_type'] = mouth_type
        return generate_mouth_func(center_x, center_y, radius_x, radius_y)

    def _generate_happy_mouth(self, center_x, center_y, radius_x, radius_y):
        mouth_width = radius_x // 2
        mouth_height = radius_y // 4
        mouth_y = center_y + radius_y // 3
        mouth_points = " ".join([
            f"{center_x - mouth_width}, {mouth_y}",
            f"{center_x}, {mouth_y + mouth_height}",
            f"{center_x + mouth_width}, {mouth_y}"
        ])
        mouth_color = self.generate_random_color()
        self.parameters['mouth_width'] = mouth_width
        self.parameters['mouth_height'] = mouth_height
        self.parameters['mouth_y'] = mouth_y
        self.parameters['mouth_color'] = mouth_color
        return f'<polygon points="{mouth_points}" fill="{mouth_color}" stroke="black" stroke-width="2"/>'

    def _generate_sad_mouth(self, center_x, center_y, radius_x, radius_y):
        mouth_width = radius_x // 2
        mouth_height = radius_y // 4
        mouth_y = center_y + radius_y // 2 - 15
        mouth_points = " ".join([
            f"{center_x - mouth_width}, {mouth_y + mouth_height}",
            f"{center_x}, {mouth_y}",
            f"{center_x + mouth_width}, {mouth_y + mouth_height}"
        ])
        self.parameters['mouth_width'] = mouth_width
        self.parameters['mouth_height'] = mouth_height
        self.parameters['mouth_y'] = mouth_y
        return f'<polygon points="{mouth_points}" fill="black" stroke="black" stroke-width="2"/>'

    def _generate_neutral_mouth(self, center_x, center_y, radius_x, radius_y):
        mouth_width = radius_x // 2
        mouth_y = center_y + radius_y // 3 + 25
        self.parameters['mouth_width'] = mouth_width
        self.parameters['mouth_y'] = mouth_y
        return f'<line x1="{center_x - mouth_width}" y1="{mouth_y}" x2="{center_x + mouth_width}" y2="{mouth_y}" stroke="black" stroke-width="4"/>'

    def __call__(self):
        """Generates an SVG string representing a face."""
        center_x = random.randint(100, 300)
        center_y = random.randint(100, 300)
        radius_x = random.randint(int(50*1.25), 100)
        radius_y = random.randint(int(80*1.25), 150)

        face_outline = self.generate_face_outline(center_x, center_y, radius_x, radius_y)
        eye_type = random.choice(list(self.eye_functions.keys()))
        eyes = self.generate_eyes(eye_type, center_x, center_y, radius_x, radius_y)
        nose = self.generate_nose(center_x, center_y, radius_x, radius_y)
        mouth_type = random.choice(list(self.mouth_functions.keys()))
        mouth = self.generate_mouth(mouth_type, center_x, center_y+20, radius_x, radius_y)

        svg = f"""
        <svg width="400" height="400">
            {face_outline}
            {"".join(eyes)}
            {nose}
            {mouth}
        </svg>
        """
        self.svg = svg
        return svg, self.parameters

    def draw(self):
        ET.dump(ET.fromstring(self.svg))
        
if __name__ == "__main__":
    sfg = RandomFaceMath()
    face, params = sfg()
    print(face)
    print(params)