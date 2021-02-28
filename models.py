from reusepatterns.prototypes import PrototypeMixin
from reusepatterns.observer import Subject, Observer
import jsonpickle


# пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Coacher(User):
    pass


# участник
class Student(User):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# Фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'coacher': Coacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Категория занятия
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Курс
class Course(PrototypeMixin, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class SmsNotifier(Observer):

    def update(self, subject: Course):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject: Course):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    def load(self, data):
        return jsonpickle.loads(data)


# Вебинар
class OnlineCourse(Course):
    pass


# Курс в студии
class InClassCourse(Course):
    pass


# Фабрика курсов
class CourseFactory:
    types = {
        'online': OnlineCourse,
        'inclass': InClassCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной класс - интерфейс проекта
class YogaSite:
    def __init__(self):
        self.coachers =[
            {
                'name': 'Мария',
                'specialization': 'хатха-йога',
                'title': 'сертифицированный тренер, стаж преподавания 6 лет',
                'description': 'Моя задача – научить вас слушать свое тело, "подружиться" с ним, сделать его чистым и прекрасным храмом для вашего духа.',
            },{
                'name': 'Владислав',
                'specialization': 'кундалини-йога',
                'title': 'сертифицированный преподаватель со стажем 8 лет',
                'description': 'Йога - огромный мир, и что бы его познать, важно правильно сделать первые шаги.',
            }
        ]
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
