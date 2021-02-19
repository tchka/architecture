import quopri
import datetime
from smart import render


def main_view(request):
    studio = request.get('studio', None)
    return '200 OK', render('index.html', studio=studio)


def coachers_view(request):


   object_list=[
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

   return '200 OK',  render('coachers.html', object_list=object_list)


def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        name = decode_value(data['name'])
        message = decode_value(data['message'])
        email = decode_value(data['email'])
        print(f'Нам пришло сообщение от {name} <{email}> с текстом {message}')

        with open ('messages.txt', 'a') as f:
            f.write(f'{datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")}, сообщение от {name} <{email}> с текстом {message}')

        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')

