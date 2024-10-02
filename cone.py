import numpy as np
from OpenGL.GL import *
import math
import ctypes

class Cone:
    def __init__(self, radius, height):
        sides = 128
        vertices = []

        # Calculate vertex positions
        theta = 2.0 * math.pi / sides
        c = math.cos(theta)
        s = math.sin(theta)
        
        # Initial coordinates on the top of the circle (in xz plane)
        x2 = radius
        z2 = 0.0
        
        # Create the strip
        for i in range(sides + 1):
            # Texture coordinate
            tx = float(i) / sides
            
            # Normal calculation
            nf = 1.0 / math.sqrt(x2 * x2 + z2 * z2)
            xn = x2 * nf
            zn = z2 * nf
            
            # Bottom vertex
            vertices.extend([x2, 0.0, z2, xn, 0.0, zn, tx, 0.0])
            # Top vertex (конус)
            if i == sides:  # Only add the top vertex once
                vertices.extend([0.0, height, 0.0, 0.0, 1.0, 0.0, tx, 1.0])
            else:
                # If not the last vertex, we still need to add the top vertex for the triangle strip
                vertices.extend([0.0, height, 0.0, 0.0, 1.0, 0.0, tx, 1.0])

            # Next position
            x3 = x2
            x2 = c * x2 - s * z2
            z2 = s * x3 + c * z2

        self._vertices_count = len(vertices) // 8
        vertices = np.array(vertices, dtype='float32')

        # OpenGL buffer setup
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.VAO)
        stride = 8 * ctypes.sizeof(ctypes.c_float)  # 8 attributes per vertex
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self._vertices_count)
        glBindVertexArray(0)
