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
        self.vertical_slice = 16
        self.horizontal_slice = 16
        self.width = 720
        self.height = 600
        self.vertices = []
        self.indices = []
        self.cellposition = []

    # 加载数据
    def loaddata(self, filepath):
        f = open(filepath)
        lines = f.readlines()
        f.close()
        x = 0
        while lines[x][0] == '#' :
            x += 1
        data = lines[x].strip().split(' ')
        while data[0] == '' or lines[x][0] == '#':
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
        neuron = self.loaddata('../src/data/Series003_cmle.CNG.swc')
        for item in neuron.keys():
            data = neuron[item]
            self.cellposition.append((data[1], data[2], data[3], data[4]))

    def window_resize(window, width, height):
        glViewport(0, 0, width, height)

    def coords_transfrom(self):
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
        self.getcoords()
        # 顶点着色器
        vertex_shader = """
                    #version 410
                    layout(location = 0) in vec3 position;
                    //layout(location = 1) in vec3 color;

                    //uniform mat4 MVP;
                    uniform mat4 ortho;
                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    //out vec3 new_color;
                    void main()
                    {
                        gl_Position = projection  * view   * ortho * model * vec4(position, 1.0f);
                        //gl_Position = MVP * ortho * vec4(position, 1.0f);
                        //new_color = color;
                    }
                    """
        # 片段着色器
        fragment_shader = """
                    #version 410
                    //uniform vec3 color;
                    out vec4 FragColor;
                    void main()
                    {
                        FragColor = vec4(0.0,1.0,0.0,1.0);
                    }
                    """
        aspect_ratio = self.width / self.height
        projection = glm.perspective(glm.radians(45), aspect_ratio, 1.0, 100.0)
        model = glm.mat4(1.0)
        le = len(self.cellposition)
        for i in range(le):
            self.Sphere(self.cellposition[i][3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(500,500,self.width,self.height)
        flag=True
        while not glfw.window_should_close(window):
            glfw.poll_events()
            # 分界线
            glClearColor(0.0, 0.0, 0.0, 1.0)
            VAO = glGenVertexArrays(1)
            glBindVertexArray(VAO)

            VBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            ver_buffer = np.array(self.vertices, dtype=ctypes.c_float)
            ind_buffer = np.array(self.indices, dtype=ctypes.c_float)
            glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * ver_buffer.itemsize, ver_buffer, GL_STATIC_DRAW)
            EBO = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.indices) * ver_buffer.itemsize, ind_buffer,
                         GL_STATIC_DRAW)
            glBindVertexArray(VAO)
            shader = shds.compileProgram(shds.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                         shds.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
            glUseProgram(shader)  # 有坑,务必放在shader编译后，否则无法使用shader

            position = glGetAttribLocation(shader, 'position')
            for i in range(le):
                # print(i)
                # 转右手坐标系
                model = glm.translate(model,glm.vec3(self.cellposition[i][0], self.cellposition[i][1], -self.cellposition[i][2]))
                view = glm.lookAt(glm.vec3(1.0, 0.0,1.0),
                                  glm.vec3(0.0, 0.0, 0.0),
                                  glm.vec3(0.0, 1.0, 0.0))

                # color = glGetAttribLocation(
                #     shader, 'color'
                # )
                ortho = glm.ortho(-1000.0, 1000.0, -1000.0, 1000.0, -500.0, 500.0)
                # print(ortho)
                # matrixID = glGetUniformLocation(shader, "MVP")
                orthoID = glGetUniformLocation(shader, "ortho")
                # glViewport(0, 0, 2 * self.width, 2 * self.height)
                model_loc = glGetUniformLocation(shader, "model")
                view_loc = glGetUniformLocation(shader, "view")
                projection_loc = glGetUniformLocation(shader, "projection")
                glUniformMatrix4fv(model_loc, 1, False, glm.value_ptr(model))
                glUniformMatrix4fv(view_loc, 1, False, glm.value_ptr(view))
                glUniformMatrix4fv(projection_loc, 1, False, glm.value_ptr(projection))
                glUniformMatrix4fv(orthoID, 1, False, glm.value_ptr(ortho))
                # glOrtho(-1000.0,1000.0, -1000.0,1000.0, -500.0,500.0)
                # glUniformMatrix4fv(matrixID, 1, False, glm.value_ptr(MVP))
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_TRUE, 3 * ver_buffer.itemsize, ctypes.c_void_p(0))
                glEnableVertexAttribArray(position)
                # MVP = projection * view * model
                # glUniformMatrix4fv(matrixID, 1, False, glm.value_ptr(MVP))
                glDrawArrays(GL_LINES,289*i, 289)

            glfw.swap_buffers(window)
        #     双缓冲
        glfw.terminate()
        os._exit(0)
    # 产生球体数据
    def Sphere(self, radius):
        # self.vertices = []
        # self.indices = []
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
    sp.coords_transfrom()
