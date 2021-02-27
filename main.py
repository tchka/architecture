import quopri
import datetime
from wsgiref.simple_server import make_server
from smart import render, Application, DebugApplication, FakeApplication
from models import YogaSite
from logging_mod import Logger, debug

site = YogaSite()
logger = Logger('main')


def secret_controller(request):
    request['studio'] = 'Oum'


front_controllers = [
    secret_controller
]

urlpatterns = {}
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
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('online', name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
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


@application.add_route('/categories/')
@debug
def categories_view(request):
    logger.log('Список категорий')
    return '200 OK', render('categories.html', objects_list=site.categories)


@application.add_route('/create-category/')
@debug
def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']

        name = decode_value(name)
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)

        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


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


def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
