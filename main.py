from smart import Application
import views

urlpatterns = {
    '/': views.main_view,
    '/coachers/': views.coachers_view,
    '/contacts/': views.contact_view,
}


def secret_controller(request):
    request['studio'] = 'Oum'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)
