import threading
import time

class ThreadConcurrency(threading.Thread):

    def __init__(self,func,args=(),kwargs={}):
        super(ThreadConcurrency,self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        # self.start()

    def run(self):
        self.result = self.func(*self.args,**self.kwargs)

    def get_execute_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception as e:
            return None

        

    def __call__(self, *args, **kwargs):
        self.start()
        return self





def database_error(request, message):
    if message == '' or message is None:
        message = '.'
    context = {
        'database_error': message,
    }
    return HttpResponseServerError(content='')


def database_error_decorator(func):
    from functools import wraps
    from django.utils.decorators import available_attrs

    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                return database_error(request, message=e.args)
        return _wrapped_view
    return decorator(func)
