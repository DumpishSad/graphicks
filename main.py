from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Начальные параметры света
light_pos = [1.0, 2.0, 1.0, 1.0]  # Положение света


def init():
    """Инициализация OpenGL"""
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Цвет фона
    glEnable(GL_DEPTH_TEST)  # Глубина
    glEnable(GL_LIGHTING)  # Включение освещения
    glEnable(GL_LIGHT0)  # Источник света 0
    glEnable(GL_COLOR_MATERIAL)  # Цвет материала
    glShadeModel(GL_SMOOTH)  # Гладкое освещение

    # Параметры света
    ambient_light = [0.2, 0.2, 0.2, 1.0]  # Фоновое освещение
    diffuse_light = [0.8, 0.8, 0.8, 1.0]  # Рассеянное освещение
    specular_light = [1.0, 1.0, 1.0, 1.0]  # Зеркальное освещение

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)  # Установка фонового света
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)  # Установка рассеянного света
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)  # Установка зеркального света

    # Материалы объектов (например, для бликов)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 50.0)  # Блеск      # Гладкое освещение


def shadow_matrix(plane, light_pos):
    """Создание матрицы проекции теней"""
    dot = np.dot(plane[:3], light_pos[:3]) + plane[3] * light_pos[3]
    shadow_mat = np.zeros((4, 4))

    for i in range(4):
        for j in range(4):
            shadow_mat[i][j] = dot - light_pos[i] * plane[j]
    return shadow_mat


def draw_wall():
    """Рисование стены"""
    glPushMatrix()
    glTranslatef(0.0, 0.0, -5.0)  # Стенка на Z = -5.0
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)  # Нормаль стены направлена вперед
    glVertex3f(-3.0, -2.0, 0.0)
    glVertex3f(3.0, -2.0, 0.0)
    glVertex3f(3.0, 2.0, 0.0)
    glVertex3f(-3.0, 2.0, 0.0)
    glEnd()
    glPopMatrix()


def draw_cube():
    """Рисование куба"""
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(-1.5, -1.0, -3.0)  # Позиция куба перед стеной
    glutSolidCube(1.0)
    glPopMatrix()


def draw_sphere():
    """Рисование шара"""
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    glTranslatef(0.0, -1.0, -3.0)  # Позиция шара перед стеной
    glutSolidSphere(0.5, 50, 50)
    glPopMatrix()


def draw_cone():
    """Рисование конуса"""
    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)
    glTranslatef(1.5, -1.0, -3.0)  # Позиция конуса перед стеной
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(0.5, 1.0, 50, 50)
    glPopMatrix()


def draw_objects():
    """Рисование всех объектов"""
    draw_cube()
    draw_sphere()
    draw_cone()


def draw_scene():
    """Отрисовка всей сцены"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Установка позиции света
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    
    # Установка камеры
    glLoadIdentity()
    gluLookAt(0.0, 1.0, 5.0,  # Положение камеры
              0.0, 0.0, -3.0, # Точка, на которую смотрит камера
              0.0, 1.0, 0.0)  # Вектор вверх

    # Рисуем стену
    draw_wall()

    # Плоскость стены: нормаль (0, 0, 1) и Z = -5.0
    plane = [0.0, 0.0, 1.0, 7.0]  # Плоскость стены (Z = -5.0)
    shadow_mat = shadow_matrix(plane, light_pos)

    # Рисуем тени
    glDisable(GL_LIGHTING)  # Отключаем освещение для теней
    glDisable(GL_DEPTH_TEST)  # Отключаем Z-буфер для теней
    glColor3f(0.0, 0.0, 0.0)  # Черный цвет для теней
    
    glPushMatrix()
    
    # Применяем матрицу проекции теней
    glMultMatrixf(shadow_mat.flatten())
    
    # Рисуем объекты, которые отбрасывают тень
    draw_objects()

    glPopMatrix()
    
    # Включаем Z-буфер и освещение обратно
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Рисуем объекты заново, чтобы они отображались поверх теней
    draw_objects()

    # Обновляем экран
    glutSwapBuffers()




def reshape(width, height):
    """Обработка изменения размеров окна"""
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def shadow_matrix(plane, light_pos):
    """Создание матрицы проекции теней"""
    dot = np.dot(plane[:3], light_pos[:3]) + plane[3] * light_pos[3]
    shadow_mat = np.zeros((4, 4))

    for i in range(4):
        for j in range(4):
            shadow_mat[i][j] = dot - light_pos[i] * plane[j]
    return shadow_mat


def keyboard(key, x, y):
    """Обработка нажатий клавиш для управления светом"""
    global light_pos
    if key == b'a':  # Свет влево
        light_pos[0] -= 0.1
    elif key == b'd':  # Свет вправо
        light_pos[0] += 0.1
    elif key == b'w':  # Свет вверх
        light_pos[1] += 0.1
    elif key == b's':  # Свет вниз
        light_pos[1] -= 0.1
    elif key == b'z':  # Свет ближе
        light_pos[2] += 0.1
    elif key == b'x':  # Свет дальше
        light_pos[2] -= 0.1

    # Перерисовываем сцену с обновленным положением света
    glutPostRedisplay()


def main():
    """Главная функция"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Shadows")

    init()

    glutDisplayFunc(draw_scene)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()
