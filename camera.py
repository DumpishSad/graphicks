import glm

# Определение возможных направлений движения камеры
FORWARD = 0
BACKWARD = 1
LEFT = 2
RIGHT = 3

# Значения по умолчанию для камеры
YAW = -90.0
PITCH = 0.0
SPEED = 9.5
SENSITIVITY = 0.01
ZOOM = 45.0

class Camera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 0.0), up=glm.vec3(0.0, 1.0, 0.0), yaw=YAW, pitch=PITCH):
        # Атрибуты камеры
        self.Position = position
        self.Front = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3(0.0, 1.0, 0.0)
        self.Right = glm.vec3(0.0, 0.0, 0.0)
        self.WorldUp = up
        self.Yaw = yaw
        self.Pitch = pitch
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM

        # Обновляем векторы камеры на основе углов Эйлера
        self.update_camera_vectors()

    # Конструктор с отдельными координатами
    @classmethod
    def from_values(cls, posX, posY, posZ, upX, upY, upZ, yaw, pitch):
        position = glm.vec3(posX, posY, posZ)
        up = glm.vec3(upX, upY, upZ)
        return cls(position, up, yaw, pitch)

    # Возвращает матрицу вида, используя углы Эйлера и матрицу "LookAt"
    def get_view_matrix(self):
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up)

    # Обрабатывает ввод с клавиатуры (абстрагированный через перечисление Camera_Movement)
    def process_keyboard(self, direction, delta_time):
        velocity = self.MovementSpeed * delta_time
        if direction == FORWARD:
            self.Position += self.Front * velocity
        if direction == BACKWARD:
            self.Position -= self.Front * velocity
        if direction == LEFT:
            self.Position -= self.Right * velocity
        if direction == RIGHT:
            self.Position += self.Right * velocity

    # Обрабатывает ввод с мыши (движение)
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.MouseSensitivity
        yoffset *= self.MouseSensitivity

        self.Yaw += xoffset
        self.Pitch += yoffset

        # Ограничиваем угол pitch, чтобы избежать переворота экрана
        if constrain_pitch:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0

        # Обновляем векторы камеры на основе углов
        self.update_camera_vectors()

    # Обрабатывает ввод с колесика мыши (скроллинг)
    def process_mouse_scroll(self, yoffset):
        self.Zoom -= yoffset
        if self.Zoom < 1.0:
            self.Zoom = 1.0
        if self.Zoom > 45.0:
            self.Zoom = 45.0

    # Вычисляет передний вектор камеры на основе углов Эйлера
    def update_camera_vectors(self):
        # Вычисление нового фронт-вектора
        front = glm.vec3(
            glm.cos(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch)),
            glm.sin(glm.radians(self.Pitch)),
            glm.sin(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        )
        self.Front = glm.normalize(front)
        # Вычисление правого и верхнего векторов
        self.Right = glm.normalize(glm.cross(self.Front, self.WorldUp))
        self.Up = glm.normalize(glm.cross(self.Right, self.Front))
