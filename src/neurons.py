'''
	@Description: draw Sphere
	@Author: yiyuan
	@Date: 2018-03-28
'''

import glm
import math

import OpenGL.GL.shaders as shds
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *


class neuron():
    def __init__(self):
        self.vertical_slice = 50
        self.horizontal_slice = 50
        self.width = 720
        self.height = 600
        self.vertices = []
        self.indices = []
        self.cellposition = [(-2000,2000,0,300)]

    # 加载数据
    def loaddata(self, filepath):
        f = open(filepath)
        lines = f.readlines()
        f.close()
        x = 0
        while lines[x][0] == '#':
            x += 1
        data = lines[x].strip().split(' ')
        neuron = {
            int(data[0]): [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]),
                           int(data[6])]}
        x += 1
        lines = lines[x:]
        for line in lines:
            data = line.strip().split(' ')
            neuron.setdefault(int(data[0]), []).extend(
                [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), int(data[6])])
            # print(neuron[float(data[0])])
        return neuron

    def getcoords(self):
        neuron = self.loaddata('../src/data/recon.swc')
        for item in neuron.keys():
            data = neuron[item]
            self.cellposition.append((data[1], data[2], data[3], data[4]))

    def window_resize(window, width, height):
        glViewport(0, 0, width, height)

    def drawSphere(self):
        self.getcoords()
        vertex_shader = """
            #version 410
            layout(location = 0) in vec3 position;
            //layout(location = 1) in vec3 color;
            
            //uniform mat4 MVP;
            uniform mat4 ortho;
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;
            out vec3 new_color;
            void main()
            {
                gl_Position = projection * view * ortho * model * vec4(position, 1.0f);
                //gl_Position = MVP * ortho * vec4(position, 1.0f);
                //new_color = color;
            }
            """
        fragment_shader = """
            #version 410
            //uniform vec3 color;
            out vec4 FragColor;
            void main()
            {
                FragColor = vec4(1.0,0.0,0.0,1.0);
            }
            """
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        window = glfw.create_window(self.width, self.height, "neuron system", None, None)
        if not window:
            glfw.terminate()
            return
        if not glfw.init():
            return
        glfw.make_context_current(window)
        # 1.投影空间和坐标归一化问题？？
        # 2.model矩阵和坐标归一化问题？？
        # glViewport(0, 0, self.width, self.height)
        # glViewport(0, 0, self.width, self.height)

        aspect_ratio = self.width / self.height
        projection = glm.perspective(glm.radians(45.0), aspect_ratio, 1.0, 100.0)
        model = glm.mat4(1.0)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho(-3000, 3000, -3000, 3000, -3000, 3000)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()
        # 分界线
        self.Sphere(self.cellposition[0][3])
        model = glm.translate(model,
                              glm.vec3(-self.cellposition[0][0], self.cellposition[0][1], self.cellposition[0][2]))
        view = glm.lookAt(glm.vec3(2.0, 2.0, 2.0),
                          glm.vec3(0.0, 0.0, 0.0),
                          glm.vec3(0.0, 0.0, 1.0))
        # view = glm.mat4(1.0)
        # view = glm.translate(view,glm.vec3(0.0,0.0,-3.0))
        MVP = projection * view * model
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        ver_buffer = np.array(self.vertices, dtype=ctypes.c_float)
        ind_buffer = np.array(self.indices, dtype=ctypes.c_float)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * ver_buffer.itemsize, ver_buffer, GL_STATIC_DRAW)
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.indices) * ver_buffer.itemsize, ind_buffer, GL_STATIC_DRAW)

        shader = shds.compileProgram(shds.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                     shds.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
        glUseProgram(shader)  # 有坑,务必放在shader编译后，否则无法使用shader

        position = glGetAttribLocation(shader, 'position')
        # color = glGetAttribLocation(
        #     shader, 'color'
        # )

        ortho = glm.ortho(-3000.0, 3000.0, -3000.0, 3000.0, -3000.0, 3000.0)
        matrixID = glGetUniformLocation(shader, "MVP")
        orthoID = glGetUniformLocation(shader, "ortho")
        glViewport(0,0,2*self.width,2*self.height)
        model_loc = glGetUniformLocation(shader, "model")
        view_loc = glGetUniformLocation(shader, "view")
        projection_loc = glGetUniformLocation(shader, "projection")
        glUniformMatrix4fv(model_loc, 1, False, glm.value_ptr(model))
        glUniformMatrix4fv(view_loc, 1, False, glm.value_ptr(view))
        glUniformMatrix4fv(projection_loc, 1, False, glm.value_ptr(projection))
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho(-3000, 3000, -3000, 3000, -3000, 3000)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        glUniformMatrix4fv(orthoID, 1, False, glm.value_ptr(ortho))
        # glUniformMatrix4fv(matrixID, 1, False, glm.value_ptr(MVP))
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_TRUE, 3 * ver_buffer.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        # glVertexAttribPointer(
        #     color, 3, GL_FLOAT, True, 6 * ver_buffer.itemsize, c_void_p(12)
        # )
        # glEnableVertexAttribArray(color)

        glBindVertexArray(VAO)

        # glClearColor(0.5, 0.6, 0.6, 1.0)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        # glEnableVertexAttribArray(0)
        while not glfw.window_should_close(window):
            glfw.poll_events()
            # glEnableClientState(GL_COLOR_ARRAY)
            # glEnableClientState(GL_INDEX_ARRAY)
            # glVertexPointer(3,GL_FLOAT,6 * ver_buffer.itemsize,self.vertices)
            # glVertexPointer(3,GL_FLOAT,3 * ver_buffer.itemsize,EBO)
            glUniformMatrix4fv(matrixID, 1, False, glm.value_ptr(MVP))
            glDrawArrays(GL_LINES, 0, int(len(self.vertices) / 3))
            # glDrawElements(GL_LINE_LOOP, int(len(self.indices)/6), GL_FLOAT, self.indices)
            # glDisableClientState(GL_VERTEX_ARRAY)

            # glDeleteVertexArrays(1, ver_buffer)
            glfw.swap_buffers(window)
            # glDisableVertexAttribArray(0)

        glfw.terminate()
        os._exit(0)

    def Sphere(self, radius):
        self.vertices = []
        self.indices = []
        # 经度
        vstep = 2 * math.pi / self.vertical_slice
        # 纬度
        hstep = math.pi / self.horizontal_slice
        start_index = 0
        current_index = 0
        # 绘制上端三角形
        for i in range(self.horizontal_slice + 1):
            start_index = current_index
            vertical_angle = hstep * i
            z_coord = radius * math.cos(vertical_angle)
            sub_radius = radius * math.sin(vertical_angle)
            for j in range(self.vertical_slice + 1):
                horizontal_angle = vstep * j
                x_coord = sub_radius * math.cos(horizontal_angle)
                y_coord = sub_radius * math.sin(horizontal_angle)
                if j == self.vertical_slice:
                    self.vertices.extend([self.vertices[start_index],
                                          self.vertices[start_index + 1],
                                          self.vertices[start_index + 2]])
                else:
                    self.vertices.extend([x_coord, z_coord, y_coord])
                current_index = current_index + 1
                if i > 0 and j > 0:
                    bottom_ring_a = (self.vertical_slice + 1) * i + j
                    bottom_ring_b = (self.vertical_slice + 1) * i + j - 1
                    top_ring_a = (self.vertical_slice + 1) * (i - 1) + j
                    top_ring_b = (self.vertical_slice + 1) * (i - 1) + j - 1
                    if j == 1:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_a)
                        self.indices.append(top_ring_b)
                    elif j == self.horizontal_slice:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_b)
                    else:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_b)


if __name__ == "__main__":
    sp = neuron()
    sp.getcoords()
    sp.drawSphere()
