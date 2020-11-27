# María Isabel Ortiz Naranjo 
# RT2: Phong Model
# Codigo proporcionado por Dennis

import random
from gl import *


# Luz
class Light(object):
    def __init__(self, position=V3(0, 0, 0), intensity=0):
        self.position = position
        self.intensity = intensity
            
# Material 
class Material(object):
    def __init__(self, diffuse=color(0,0,0), albedo=(1,0), spec=0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec

class Raytracer(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.models = []
        self.currentbg_color = WHITE
        self.light = None
        self.clear()

    def glInit(self, width, height):
        return

    def glViewPort(self, x, y, width, height):
        self.xw = x
        self.yw = y
        self.widthw = width
        self.heightw = height

    def clear(self):
        self.pixels = [[self.currentbg_color for x in range(self.width)] for y in range(self.height)]
        
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.pixels)
    
    def cast_ray(self, orig, direction):
        material, intersect = self.scene_intersect(orig, direction)

        if material is None:
            return self.currentbg_color

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        offset_normal = mul(intersect.normal, 1.1)  
        shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        shadow_intensity = 0

        if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
        max(0, -dot(reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        return (diffuse + specular)

    def render(self):
        fov = int(pi / 2)
        for y in range(self.height):
            for x in range(self.width):
                i = (
                    (2 * (x + 0.5) / self.width - 1)
                    * tan(fov / 2)
                    * self.width
                    / self.height
                )
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.pixels[y][x] = self.cast_ray(V3(1, 0, 0), direction)

    def show(self, filename='final.bmp'):
        self.render()
        self.write(filename)

    def point(self, x, y, color = None):
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass
    
    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.models:
            hit = obj.ray_intersect(orig, direction)
            if hit is not None: 
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect


class Intersect(object):
    def __init__(self, distance=0, point=None, normal= None):
        self.distance = distance
        self.point = point
        self.normal = normal


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, direction):
        L = sub(self.center, orig)
        tca = dot(L, direction)
        l = length(L)
        d2 = l**2 - tca**2

        if d2 > self.radius**2:
            return None

        thc = (self.radius**2 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        hit = sum(orig, mul(direction, t0))
        normal = norm(sub(hit, self.center))

        return Intersect(
            distance=t0,
            point=hit,
            normal=normal
        )
    
def cast_ray(self, orig, direction):
    impacted_material, intersect = self.scene_intersect(orig, direction)
    
    if impacted_material is None:
        return self.clearC

    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    offset_normal = mul(intersect.normal, 1.1)

    if dot(light_dir, intersect.normal) < 0:
        shadow_orig = sub(intersect.point, offset_normal)
    else:
        shadow_orig = sum(intersect.point, offset_normal)
        
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
        shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)
        
    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (max(0, -dot(reflection, direction))**impacted_material.spec)

    diffuse = impacted_material.diffuse * intensity * impacted_material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * impacted_material.albedo[1]
    return diffuse + specular


BLACK = color(0, 0, 0)
BACK = color(255, 204, 204)
WHITE = color(255, 255, 255)


r = Raytracer(500, 500)

ivory = Material(diffuse=color(100, 100, 80), albedo=(0.5,  0.4), spec=30)
rubber = Material(diffuse=color(180, 0, 0), albedo=(0.6,  0.3), spec=10)
white = Material(diffuse=color(255, 255, 255), albedo=(0.5,  0.4), spec=30)
brown = Material(diffuse=color(162, 81, 10), albedo=(0.2,  0.3), spec=10)
eye = Material(diffuse=color(50, 50, 50), albedo=(0.2,  0.3), spec=10)
broown = Material(diffuse=color(255, 204, 153), albedo=(0.2,  0.3), spec=10)


r.light = Light(
    position = V3(20, 15, 30),
    intensity = 1.4
)

r.current_color = BACK
r.models = [

     #Osito blanco
    Sphere(V3(-3.2, -1.3, -15), 2, white),
    Sphere(V3(-1.5, 0, -14.5), 1.1, white),
    Sphere(V3(-4.9, 0, -14.5), 1.1, white),
    Sphere(V3(-2.1, -2.6, -14.1), 1.1, white),
    Sphere(V3(-4.5, -2.6, -14.1), 1.1, white),
    Sphere(V3(-3.2, 1.6, -14.9), 1.7, white),
    Sphere(V3(-3.2, 1.6, -14.9), 1.7, white),
    Sphere(V3(-2.2, 2.7, -14.4), 0.7, white),
    Sphere(V3(-4.2, 2.7, -14.4), 0.7, white),
    Sphere(V3(-3.2, 1.3, -13.3), 0.6, white),
    Sphere(V3(-3.6, 2.1, -13.5), 0.2, eye),
    Sphere(V3(-2.8, 2.1, -13.5), 0.2, eye),
    
    #Osito Cafe 
    Sphere(V3(3.2, -1.3, -15), 2, rubber),
    Sphere(V3(4.9, 0, -14.5), 1.1, brown),
    Sphere(V3(1.5, 0, -14.5), 1.1, brown),
    Sphere(V3(4.3, -2.6, -14.1), 1.1, brown),
    Sphere(V3(1.9, -2.6, -14.1), 1.1, brown),
    Sphere(V3(3.2, 1.6, -14.9), 1.7, brown),
    Sphere(V3(4.2, 2.7, -14.4), 0.7, broown),
    Sphere(V3(2.2, 2.7, -14.4), 0.7, broown),
    Sphere(V3(3.2, 1.3, -13.52), 0.6, broown),
    Sphere(V3(2.8, 2.1, -13.5), 0.2, eye),
    Sphere(V3(3.6, 2.1, -13.5), 0.2, eye),
]

r.show()
