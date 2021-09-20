import datetime
import functools
import inspect
import json
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.views import View


JSON_DUMPS_PARAMS = {
    "ensure_ascii": False
}

def ret(json_object, status = 200):

	""" Віддає JSON з правильними HTTP заголовками """

	return JsonResponse(
		json_object,
		status = status,
		safe= not isinstance(json_object, list),
		json_dumps_params=JSON_DUMPS_PARAMS
	)	


def error_response(exception):
	
	""" Форматує HTTP відповідь з описом помилки """

	res = {"errorMessage":str(exception),
			"traceback": traceback.format_exc()	}
	return ret(res, status=400)


def base_views(fn):

    """ Decorator for all views hangling exceptions """

    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
    	try:
    		with transaction.atomic():
    			return fn(request, *args, **kwargs)
    	except Exception as e:
    		return error_response(e)

    return inner		

