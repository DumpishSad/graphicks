import math
import random
from OpenGL.GL import *
import glm
import glfw
import numpy as np

from camera import Camera, FORWARD, BACKWARD, RIGHT, LEFT
from shader import Shader
from texture import load_texture
from cube import Cube
from sphere import Sphere
from cone import Cone
from surface import Surface

# Конфигурация теней
SHADOW_WIDTH, SHADOW_HEIGHT = 1024, 1024

# Камера

camera = Camera(glm.vec3(0.0, 1.0, 6.0))
lastX, lastY = 800 / 2.0, 600 / 2.0
firstMouse = True
deltaTime = 0.0
lastFrame = 0.0

# Модели
surface = None
cube = None
sphere = None
cone = None
cone_textureID = None 

# Настройка света
lightPos = glm.vec3(-5.0, 4.0, -2.0)  # Определяем начальную позицию света
lightSpeed = 0.5  # Скорость перемещения света


def setup_viewport(window):
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

def key_callback(window, key, scancode, action, mods):
    global deltaTime, lightPos  # Объявляем lightPos глобальной
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_W:
        camera.process_keyboard(FORWARD, deltaTime)
    if key == glfw.KEY_S:
        camera.process_keyboard(BACKWARD, deltaTime)
    if key == glfw.KEY_A:
        camera.process_keyboard(LEFT, deltaTime)
    if key == glfw.KEY_D:
        camera.process_keyboard(RIGHT, deltaTime)

    if key == glfw.KEY_UP and action != glfw.RELEASE:  # Вверх
        lightPos.y += lightSpeed
    if key == glfw.KEY_DOWN and action != glfw.RELEASE:  # Вниз
        lightPos.y -= lightSpeed
    if key == glfw.KEY_LEFT and action != glfw.RELEASE:  # Влево
        lightPos.x -= lightSpeed
    if key == glfw.KEY_RIGHT and action != glfw.RELEASE:  # Вправо
        lightPos.x += lightSpeed
    if key == glfw.KEY_PAGE_UP and action != glfw.RELEASE:  # Двигаем свет вперед
        lightPos.z += lightSpeed
    if key == glfw.KEY_PAGE_DOWN and action != glfw.RELEASE:  # Двигаем свет назад
        lightPos.z -= lightSpeed

def scroll_callback(window, xoffset, yoffset):
    camera.process_mouse_scroll(float(yoffset))

def cursor_position_callback(window, xpos, ypos):
    global firstMouse, lastX, lastY
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) != glfw.PRESS:
        return
    if firstMouse:
        lastX, lastY = xpos, ypos
        firstMouse = False
    xoffset, yoffset = xpos - lastX, lastY - ypos
    lastX, lastY = xpos, ypos
    camera.process_mouse_movement(float(xoffset), float(yoffset))

def render_scene(shader):
    global textureID, textureID2, cone_textureID  # Добавлено cone_textureID
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureID)
    # Рендеринг пола
    model = glm.mat4(1.0)
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 128.0)
    surface.render()
    
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureID2)

    # Рендеринг куба
    model = glm.mat4(1.0)
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 64.0)
    cube.render()

    # Рендеринг сферы
    model = glm.translate(glm.mat4(1.0), glm.vec3(3.0, 1.0, 0.0))  # Позиция сферы
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.5, 0.5, 0.5))    # Увеличиваем окружающий свет
    shader.set_vec3("material.diffuse", glm.vec3(0.7, 0.7, 0.7))    # Увеличиваем рассеянное освещение
    shader.set_vec3("material.specular", glm.vec3(1.0, 1.0, 1.0))
    shader.set_float("material.shininess", 128.0)
    sphere.render()

    # glActiveTexture(GL_TEXTURE0)
    # glBindTexture(GL_TEXTURE_2D, cone_textureID)

    # Рендеринг конуса
    model = glm.translate(glm.mat4(1.0), glm.vec3(-3.0, 0.0, 0.0))  # Позиция конуса
    shader.set_mat4("model", model)
    shader.set_vec3("material.ambient", glm.vec3(0.3, 0.3, 0.3))    # Небольшой ambient для общей подсветки
    shader.set_vec3("material.diffuse", glm.vec3(0.8, 0.8, 0.8))    # Высокое значение diffuse для сильного рассеивания света
    shader.set_vec3("material.specular", glm.vec3(0.0, 0.0, 0.0))   # Полностью убираем specular для устранения бликов
    shader.set_float("material.shininess", 1.0)    
    cone.render()

def main():
    global deltaTime, lastFrame, surface, cube, sphere, cone, textureID, textureID2, cone_textureID

    if not glfw.init():
        raise Exception("GLFW initialization failed")

    window = glfw.create_window(800, 600, "Lab1", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)
    setup_viewport(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Загрузка текстур и шейдеров
    textureID = load_texture("wood.png")
    # cone_textureID = load_texture("cone_texture.png") 
    textureID2 = load_texture("briks.png")
    shader = Shader("shading.vert", "shading.frag")
    simpleDepthShader = Shader("depth.vert", "depth.frag")
    depth_map_fbo = glGenFramebuffers(1)
    depth_map = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

    border_color = [1.0, 1.0, 1.0, 1.0]
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)

    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glEnable(GL_DEPTH_TEST)

    shader.use()
    shader.set_int("diffuseTexture", 0)
    shader.set_int("shadowMap", depth_map_fbo)
    shader.set_vec3("lightColor", glm.vec3(0.6))

    shader.set_vec3("material.ambient", glm.vec3(0.6, 0.6, 0.6))
    shader.set_vec3("material.diffuse", glm.vec3(1.0, 0.5, 0.31))
    shader.set_vec3("material.specular", glm.vec3(0.5, 0.5, 0.5))
    shader.set_float("material.shininess", 64.0)

    surface = Surface()
    cube = Cube()
    sphere = Sphere()  # Создаем объект сферы
    cone = Cone(1.0, 1.5)      # Создаем объект конуса

    # Основной цикл рендеринга
    while not glfw.window_should_close(window):
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        lightProjection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 15.5)
        lightView = glm.lookAt(lightPos, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
        lightSpaceMatrix = lightProjection * lightView

        shader.set_vec3("lightPos", lightPos)
        shader.set_mat4("lightSpaceMatrix", lightSpaceMatrix)

        simpleDepthShader.use()
        simpleDepthShader.set_mat4("lightSpaceMatrix", lightSpaceMatrix)

        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textureID)

        glCullFace(GL_FRONT)
        render_scene(simpleDepthShader)
        glCullFace(GL_BACK)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        setup_viewport(window)


        shader.use()
        projection = glm.perspective(glm.radians(camera.Zoom), 800 / 600, 0.1, 100.0)
        view = camera.get_view_matrix()
        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, depth_map)

        render_scene(shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
