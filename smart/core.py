import os


class Application:

    def add_route(self, url):
        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns, front_controllers):
        """
        :param urlpatterns: dict url: view
        :param front_controllers: list
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)

        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if len(path.split('/')) == 3 and path.split('/')[1] == 'static':
            dir = os.getcwd()
            # dir = os.path.split(dir)[0]
            if path[0] == '/':
                path = path[1:]
            static_file = os.path.join(dir, path)
            if os.path.isfile(static_file):
                print('yes')
                with open(static_file, 'r', encoding="utf-8") as f:
                    file_content = f.read()

                extension = path.split('.')[-1]
                if extension == 'css':
                    start_response('200 OK', [('Content-Type', 'text/css')])
                    return [file_content.encode('utf-8')]
                elif extension == 'jpg':
                    start_response('200 OK', [('Content-Type', 'image/jpeg')])
                    return [file_content.encode('utf-8')]
                elif extension == 'js':
                    start_response('200 OK', [('Content-Type', 'application/javascript')])
                    return [file_content.encode('utf-8')]
                else:
                    start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
                    return [b"Not Found"]
            else:
                start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
                return [b"Not Found"]

        if path[-1] != '/':
            path = f'{path}/'

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            for controller in self.front_controllers:
                controller(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]
