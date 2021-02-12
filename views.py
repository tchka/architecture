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
