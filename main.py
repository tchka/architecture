import quopri
import datetime
from smart import render, Application, DebugApplication, FakeApplication
from models import YogaSite, BaseSerializer, EmailNotifier, SmsNotifier
from smart.smartcbv import ListView, CreateView
from logging_mod import Logger, debug
from smartorm import UnitOfWork
from mappers import MapperRegistry

site = YogaSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


def secret_controller(request):
    request['studio'] = 'Oum'


front_controllers = [
    secret_controller
]


class StudentListView(ListView):
    # queryset = site.students
    template_name = 'students.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()

class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


class CategoryListView(ListView):
    # queryset = site.students
    template_name = 'categories.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()

class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = decode_value(name)
        new_obj = site.create_category('category', name)
        site.categories.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


urlpatterns = {
    '/create-category/': CategoryCreateView(),
    '/categories/': CategoryListView(),
    '/students/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
}
application = Application(urlpatterns, front_controllers)


# application = DebugApplication(urlpatterns, front_controllers)
# application = FakeApplication(urlpatterns, front_controllers)

@application.add_route('/')
@debug
def main_view(request):
    logger.log('Главная страница')
    return '200 OK', render('index.html')


@application.add_route('/courses/')
@debug
def courses_view(request):
    logger.log('Список курсов')
    print(f'Список курсов - {site.courses}')
    return '200 OK', render('courses.html', objects_list=site.courses)


@application.add_route('/create-course/')
@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        name = decode_value(name)
        category_id = data.get('category_id')
        print(category_id)
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('online', name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


@application.add_route('/copy-course/')
@debug
def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('courses.html', objects_list=site.courses)


# @application.add_route('/categories/')
# @debug
# def categories_view(request):
#     logger.log('Список категорий')
#     return '200 OK', render('categories.html', objects_list=site.categories)
#
#
# @application.add_route('/create-category/')
# @debug
# def create_category(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#
#         name = decode_value(name)
#         category_id = data.get('category_id')
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#
#         site.categories.append(new_category)
#         return '200 OK', render('create_category.html')
#     else:
#         categories = site.categories
#         return '200 OK', render('create_category.html', categories=categories)


@application.add_route('/coachers/')
@debug
def coachers_view(request):
    logger.log('Список тренеров')
    # object_list=[
    #     {
    #         'name': 'Мария',
    #         'specialization': 'хатха-йога',
    #         'title': 'сертифицированный тренер, стаж преподавания 6 лет',
    #         'description': 'Моя задача – научить вас слушать свое тело, "подружиться" с ним, сделать его чистым и прекрасным храмом для вашего духа.',
    #     },{
    #         'name': 'Владислав',
    #         'specialization': 'кундалини-йога',
    #         'title': 'сертифицированный преподаватель со стажем 8 лет',
    #         'description': 'Йога - огромный мир, и что бы его познать, важно правильно сделать первые шаги.',
    #     }
    # ]

    return '200 OK', render('coachers.html', objects_list=site.coachers)


@application.add_route('/contacts/')
@debug
def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        name = decode_value(data['name'])
        message = decode_value(data['message'])
        email = decode_value(data['email'])
        print(f'Нам пришло сообщение от {name} <{email}> с текстом {message}')

        with open('messages.txt', 'a') as f:
            f.write(
                f'{datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")}, сообщение от {name} <{email}> с текстом {message}')

        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')

@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()

def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')


