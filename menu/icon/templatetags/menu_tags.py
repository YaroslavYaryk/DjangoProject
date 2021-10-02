from django import template
from icon.models import *
from django.db.models import Count, F


register = template.Library()

@register.simple_tag()
def get_category():
	return Category.objects.all()

@register.simple_tag()
def get_category_spec():
	return Category.objects.annotate(publ = F("woman__is_published"), cnt = Count("woman", filter = Q(publ__gt = 0))).filter(cnt__gt = 0)

@register.simple_tag()
def get_news_sort():	
	return Woman.objects.filter(is_published = True)[1:]

@register.simple_tag()
def get_news():
	return Woman.objects.filter(is_published = True).select_related("cat")

@register.inclusion_tag("icon/new/show_category_list.html")
def get_categories_list(sort = None):
	if not sort:
		cats = Category.objects.annotate(publ = F("woman__is_published"), cnt = Count("woman", filter = Q(publ__gt = 0))).filter(cnt__gt = 0)	
	else:
		cats = Category.objects.order_by(sort)	
	return {"cats":cats}	


@register.inclusion_tag("icon/new/get_top_chart.html")
def get_top_chart():

	order = Woman.objects.order_by("ip").last()
	return {"order": order}

@register.inclusion_tag("icon/new/get_most_liked.html")
def get_most_liked():

	queryset = Woman.objects.all()
	res = queryset.first()
	for elem in queryset:
		if elem.likes.count() > res.likes.count():
			res = elem


	return {"order": res}
