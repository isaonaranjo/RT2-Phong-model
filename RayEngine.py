# Maria Isabel Ortiz Naranjo
# Carne: 18176

from raytracing import Raytracer
from raytracing import Material
from raytracing import Light
from raytracing import Sphere
from raytracing import Color
from raytracing import V3

# Colors & Materials

RED = Color(255, 52, 52)
BROWN = Color(200, 94, 38)
LIGHT_BROWN = Color(245, 180, 150)
LIGHT_CYAN = Color(224, 255, 255)
WHITE = Color(248, 248, 248)
GRAY = Color(200, 200, 200)
BLACK = Color(40, 40, 40)
GREEN = Color(154, 255, 52)

punto_negro = Material(diffuse=BLACK, albedo=(0.64, 0.36), spec=5)
rojo = Material(diffuse=RED, albedo=(0.64, 0.36), spec=15)
nieve = Material(diffuse=WHITE, albedo=(0.86, 0.86), spec=30)
metalico = Material(diffuse=GRAY, albedo=(1, 1), spec=30)

# Render
render = Raytracer(800, 800)
render.light = Light(position=V3(-4, -0.5, 20), intensity=1.5)
render.background_color = WHITE
render.scene = [

    # Cuerpo
    #Sphere(V3(0, 1.8, -6), 0.76, nieve),
    Sphere(V3(0, 0.4, -6), 0.94, nieve),
    Sphere(V3(0, -1.74, -8), 1.8, nieve),

    # Cabeza
    Sphere(V3(0.24, 2.08, -6), 0.06, punto_negro),
    Sphere(V3(-0.24, 2.08, -6), 0.06, punto_negro),
    Sphere(V3(0.24, 2.08, -6), 0.14, metalico),
    Sphere(V3(-0.24, 2.08, -6), 0.14, metalico), 
    Sphere(V3(0, 1.82, -6), 0.16, rojo),
    Sphere(V3(-0.3, 1.62, -6), 0.06, punto_negro),
    Sphere(V3(-0.14, 1.48, -6), 0.06, punto_negro),
    Sphere(V3(0.14, 1.48, -6), 0.06, punto_negro),
    Sphere(V3(0.3, 1.62, -6), 0.06, punto_negro),
   
    # Complementos de Cuerpo

    Sphere(V3(0, 0.9, -6), 0.08, punto_negro),
    Sphere(V3(0, 0.2, -6), 0.16, punto_negro),
    Sphere(V3(0, -1.42, -6), 0.24, punto_negro),

]

render.finish()