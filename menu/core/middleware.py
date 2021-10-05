from django.shortcuts import render
from loguru import logger as log


# log.add("/home/yaroslav/Programming/Python/Django/menu/logging/log_middleware.log",
#         enqueue=True, level="ERROR", rotation="10 MB")

class ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    # def process_exception(self, request, exception):

    #     if request.path == "/":
    #         button = "Send_feedback"
    #         error = "Sorry for this, please send message to make it allright"
    #     else:
    #         error = exception.args[0]
    #         button = "Home"

    #     log.error(exception)    

    #     return render(request, "icon/error.html", context={"error": error, "button": button})
