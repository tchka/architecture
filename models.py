from reusepatterns.prototypes import PrototypeMixin


# пользователь
class User:
    pass


# преподаватель
class Coacher(User):
    pass


# студент
class Student(User):
    pass


# Фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'coacher': Coacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


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
class Course(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# Интерактивный курс
class OnlineCourse(Course):
    pass


# Курс в записи
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
        self.coachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

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
        return None
