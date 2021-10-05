from rest_framework.response import Response
from rest_framework.serializers import Serializer
from menu.settings import CRITICAL
from re import I, search
from django.contrib.messages.api import add_message
from django.core.mail import message, send_mail
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseNotFound
from .models import Woman, Category
from django.db.models import Q
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
import json
from django.template import RequestContext
from core.views import base_views
from loguru import logger as log
from .utils import menu
from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_headers
from rest_framework.views import APIView
from .serializers import WomanSerializer, WomanDetailSerializer,CategorySerializer
from rest_framework.viewsets import ModelViewSet


comment_is_liked = []

order = ""
# log.add("/home/yaroslav/Programming/Python/Django/menu/logging/log.log",
#         enqueue=True, level="DEBUG", rotation="10 MB")


class Home_page(DataMixin, CapMixin, ListView):

    """class for depicting all news, start page"""

    model = Woman
    template_name = 'icon/home.html'
    # can put only static files (unchanged)
    # extra_context = {"title": "Home page"}
    mix_prop = "home page"
    context_object_name = "post"

    search_query = ""
    order_query = ""

    # to add some list to our page

    def get_context_data(self, *, object_list=None, **kwargs):

        order = ""
        with open("icon/order_folders/order.txt", "r", encoding="utf-8") as file:
            order = file.read()

        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(
            title=self.get_title(),
            first=Woman.objects.filter(is_published=True).first(), order=order,
            order_list=self.order_list)
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request, *args, **kwargs):  # get all the consistence of input field

        global order
        self.search_query = request.GET.get("search", "")
        self.order_query = request.GET.get("order", "")
        if self.order_query and order != self.order_query:
            order = self.order_query

        with open("icon/order_folders/search.txt", "w") as f:
            if self.search_query:
                f.write(self.search_query)

        with open("icon/order_folders/order.txt", "w") as f:
            if order:
                f.write(order)

        return super(Home_page, self).get(request, *args, **kwargs)

    choice_order = {
        "most popular 👇": "-ip",
        "most popular 👆": "ip",
        "most liked 👆": "likes",
        "most liked 👇": "-likes"
    }

    order_list = ["newest", "most popular 👇",
                  "most popular 👆", "most liked 👆", "most liked 👇"]

    def get_choice(self):

        result = ''
        with open("icon/order_folders/order.txt", "r") as f:
            result = f.read()
        try:
            a = self.choice_order[result]
        except KeyError:
            return "-creation_date"
        return a

    def get_queryset(self):
        if self.search_query:  # if someth is written in search we view all similarity
            return Woman.objects.filter(Q(is_published=True), Q(title__icontains=self.search_query) | Q(content__icontains=self.search_query)).order_by(self.get_choice()).select_related("cat")

        # it's only for specific model
        return Woman.objects.filter(is_published=True).order_by(self.get_choice()).select_related("cat")
        # to find only those element we need

@never_cache
def storage(request):

    contact_list = Woman.objects.all()
    paginator = Paginator(contact_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "icon/storage.html", {"page_obj": page_obj, "first_link": page_obj.paginator.page(1).object_list})


class NewsNyCategory(DataMixin, DetailView, CreateView):

    """ class for getting information about specific news """

    model = Woman
    slug_url_kwarg = "slug_id"
    template_name = "icon/read_more.html"
    context_object_name = "post"
    form_class = WomanCommentForm
    success_message = "Comment added successfully"
    error_message = "Adding error"
    username = ""

    # to add some list to our page
    def get_context_data(self, *, object_list=None, **kwargs):

        post = Woman.objects.select_related().get(
            slug=self.kwargs["slug_id"])  # get current post
        # if not exists
        if not IpModel.objects.filter(ip=get_client_ip(self.request), post_news=post):
            IpModel.objects.create(ip=get_client_ip(
                self.request), post_news=post)  # create new one

        for elem in LikedComment.objects.all().select_related():
            if self.request.user.is_authenticated:
                if elem.user != self.request.user:
                    elem.user = self.request.user
                    elem.choice = "No"  # no  like
                    elem.save()

        liked = 0

        global chioce, comment_is_liked

        if self.request.user != "AnonymousUser":
            try:
                liked = WomanLike.objects.filter(user=self.request.user, post=Woman.objects.select_related(
                ).get(slug=self.kwargs["slug_id"])).select_related("post", "user")
                # get like if its liked
            except TypeError:
                pass
        else:
            liked = 0
        user = self.request.user

        if user.is_authenticated:
            comment_likes=LikedComment.objects.filter(
                                          user=self.request.user).select_related("post_comment", "user")

        else:
            comment_likes = None                                  
                                      

        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(image=WomanImage.objects.filter(post__slug=self.kwargs["slug_id"]).select_related("post"),
                                      first=WomanImage.objects.filter(
                                          post__slug=self.kwargs["slug_id"]).select_related("post").first(),
                                      comments=WomanComment.objects.annotate(len=Length(F('comment'))).filter(
                                          post__slug=self.kwargs["slug_id"]).select_related('post'),
                                      is_liked=liked,
                                     comment_likes = comment_likes,
                                     user = user)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):

        storage = {'username': request.POST.get('username'),
                   "comment": request.POST.get('comment')}
        post_id = Woman.objects.select_related().get(
            slug=self.kwargs["slug_id"]).id
        new_comment = WomanComment(username=storage["username"],
                                   comment=storage["comment"],
                                   post_id=post_id)  # create new post
        # create like(choice = No)
        like = LikedComment(user=self.request.user, post_comment=new_comment)

        with open("icon/order_folders/post.txt", "w") as f:
            f.write(self.kwargs["slug_id"])

        if self.request.user.is_authenticated:  # user is not Anonim user
            if ("pause" not in request.session):
                request.session.set_expiry(60)
                request.session["pause"] = True
                new_comment.save()  # save changes database
                like.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Comment successfully left')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Wait until time is up')
        else:
            messages.add_message(request, messages.WARNING,
                                 'you"re not signed in ')
            return redirect("sign_in")

        return redirect('post', slug_id=self.kwargs["slug_id"])

    def get_queryset(self):  # ???
        return Woman.objects.filter(slug=self.kwargs["slug_id"]).select_related()

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()

        initial['username'] = self.request.user.username
        initial['comment'] = None

        return initial


order2 = ""


class WomanCategory(DataMixin, ListView):

    """Class shows news inspecific category"""
    model = Category
    template_name = "icon/show_categories.html"
    context_object_name = "storage"
    search_query = ""
    order_query = ""

    def get(self, request, *args, **kwargs):  # get all the consistence of input field
        global order2
        self.search_query = request.GET.get("search", "")
        self.order_query = request.GET.get("order2", "")
        if self.order_query and order2 != self.order_query:
            order2 = self.order_query

        with open("icon/order_folders/order2.txt", "w") as f:
            if order2:
                f.write(order2)

        return super(WomanCategory, self).get(request, *args, **kwargs)

    choice_order = {
        "most popular 👇": "-ip",
        "most popular 👆": "ip",
        "most liked 👆": "likes",
        "most liked 👇": "-likes"
    }

    order_list = ["newest", "most popular 👇",
                  "most popular 👆", "most liked 👆", "most liked 👇"]

    def get_choice(self):

        result = ''
        with open("icon/order_folders/order2.txt", "r") as f:
            result = f.read()
        try:
            a = self.choice_order[result]
        except KeyError:
            return "-creation_date"
        return a

    def render_to_response(self, context, **response_kwargs):
        response = super(WomanCategory, self).render_to_response(
            context, **response_kwargs)
        response.set_cookie(str(self.kwargs["category_name"]).replace(
            " ", "_"), 'beloved_category')
        return response

    def get_queryset(self):

        print(self.get_choice())

        if self.search_query:  # if someth is written in search we view all similarity
            return Woman.objects.filter(Q(cat__slug=self.kwargs["category_name"]),
                                        Q(is_published=True),
                                        Q(title__icontains=self.search_query) | Q(content__icontains=self.search_query)).order_by(self.get_choice()).select_related("cat")

        # it's only for specific model
        return Woman.objects.filter(cat__slug=self.kwargs["category_name"],
                                    is_published=True).select_related("cat")
        # to find only those element we need

    def get_context_data(self, *, object_list=None, **kwargs):

        order = ""
        with open("icon/order_folders/order2.txt", "r", encoding="utf-8") as file:
            order = file.read()

        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(cat_slug=self.kwargs["category_name"],
                                      cat = Category.objects.get(slug = self.kwargs["category_name"]),
                                      order=order,
                                      order_list=self.order_list)
        return dict(list(context.items()) + list(c_def.items()))


class WomanEditView(DataMixin, SuccessMessageMixin, UpdateView):
    model = Woman
    form_class = NewModelForm
    # success_url = reverse_lazy("home")
    slug_url_kwarg = "slug_name"
    success_message = "Post upgrated successfully"
    error_message = "There are some problem with updating this post"
    template_name = "icon/edit_page_model.html"
    # fields = ["title", "content", "photo", "cat"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class NewsStore(DataMixin, CapMixin, CreateView):

    """class create form for adding news"""

    form_class = NewModelForm
    template_name = "icon/add_page_model.html"
    success_url = reverse_lazy("home")
    mix_prop = "add post"
    login_url = "sign_in"
    required_css_class = 'required'
    error_message = 'Something went wrong'

    # to add some list to our page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(
            title=self.get_title(), ico="menu/img/ico/home_pink.png")
        return dict(list(context.items()) + list(c_def.items()))


class WomanDeleteView(DataMixin, SuccessMessageMixin, DeleteView):
    model = Woman
    success_url = reverse_lazy("home")
    slug_url_kwarg = "slug_title"
    template_name = "icon/delete_post.html"
    success_message = "post deleted successfully"
    error_message = "There are some problem with deleting this post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(
            title=self.kwargs["slug_title"], ico="menu/img/ico/home_pink.png")
        return dict(list(context.items()) + list(c_def.items()))


class WomanAbout(DataMixin, TemplateView):
    template_name = "icon/about.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


@never_cache
@base_views
def get_someth(request):

    resp = HttpResponse("Здecь будет",
                        content_type='text/plain; charset=utf-8')
    resp. write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


class RegisterUser(DataMixin, SuccessMessageMixin, CreateView):
    """Show register form"""

    form_class = RegisterUserForm
    template_name = 'icon/register.html'
    success_url = reverse_lazy("send_mail_register")
    success_message = "User added successfully"
    error_message = "Registration error"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_user_context(
            title="Registration", ico="menu/img/ico/home_pink.png")
        return dict(list(context.items()) + list(c_def.items()))


@never_cache
def send_mail_register(request):

    user = User.objects.order_by("-id").first() #get last registered
    message = "Thanks for taking our site, i'm really dekightful that you're here, keep on developing, you've got this"
    user.email_user('Welcome', message , fail_silently=True)

    return HttpResponseRedirect(reverse("sign_in"))



class LoginUser(DataMixin, SuccessMessageMixin, LoginView):

    """Autorization class"""

    form_class = LoginUserForm
    template_name = 'icon/sign_in.html'
    error_message = "Something went wrong"
    user = ""
    success_message = f"Successfully sign in"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_user_context(
            title="Sign in", ico="menu/img/ico/home_pink.png")

        return dict(list(context.items()) + list(c_def.items()))


class LogoutUser(LogoutView, SuccessMessageMixin):

    next_page = "home"
    success_message = "Logout successfully"


class ProfileView(DataMixin, ListView):

    model = User
    template_name = "icon/profile.html"

    def get_context_data(self, *args, **kwargs):
        try:
            user = self.request.user
        except:
            user = None    
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_user_context(
            user = user,
            title="Profile",
            post=Woman.objects.raw(
                "SELECT id, title FROM icon_woman")[0],
            last_post=Woman.objects.raw("""SELECT * from icon_woman
                ORDER by  creation_date DESC""")[0])
        return dict(list(context.items()) + list(c_def.items()))


@never_cache
@base_views
def likeView(request, pk):
    """ function for adding like to our post """

    response = HttpResponseRedirect(reverse("post", args=[str(pk)]))

    post_id = request.GET.get("likeId", "")
    user = request.user  # get user
    try:
        post = Woman.objects.get(slug=pk)  # get post
        liked = False
        like = WomanLike.objects.filter(user=user, post=post).select_related(
            "post", "user")  # get queryset with user=user, post=post

        if like:
            like.delete()  # thre is like put
        else:
            liked = True
            WomanLike.objects.create(user=user, post=post)  # create like
    except TypeError:  # is not signed in
        messages.add_message(request, messages.WARNING,
                             'to put like you need to sign in first ')
        return response

    response.set_cookie(post.title[:20].replace(" ", "_"), "like.com") if liked else response.set_cookie(
        post.title[:20].replace(" ", "_"), "dislike.com")
    return response


@never_cache
@base_views
def commentLikeView(request, like_id):  # press like
    """ make hitting comment like """

    global users_storage, comment_is_liked
    comment = get_object_or_404(WomanComment, pk=like_id)  # get comment
    user = request.user  # get user
    like = 1

    try:
        like = LikedComment.objects.filter(
            post_comment=comment, user=user).first()  # get queryset of first
        # post vith post_comment = comment and user = user
    except Exception:
        like = 0

    if not like:
        like = LikedComment.objects.create(post_comment=comment, user=user)
        # there is no such like - create new

    if like.choice == "No":  # not liked
        comment.likes.add(request.user)  # add like
        like.delete()  # delete previous and create new with choice = Yes
        like = LikedComment.objects.create(
            post_comment=comment, user=user, is_liked=True, choice="Yes")

    else:
        comment.likes.remove(request.user)  # delete like
        like.delete()  # delete previous and create new with choice = No
        like = LikedComment.objects.create(
            post_comment=comment, user=user, is_liked=True, choice="No")

    return redirect("post", slug_id=f"{comment.post.slug}")


def get_client_ip(request):  # get current ip address

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@never_cache
def show_ip(request):  # just for check ip address
    a = get_client_ip(request)
    return HttpResponse(f"ip is {a} ")


@never_cache
# @base_views
def tmp_views(request):

    # a  = 1 /0
    post = Woman.objex.all()
    log.critical(post)
    return JsonResponse({"success": True})


@never_cache
def django_boottstrap(request):

    form = ""

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = NewsForm()
    return render(request, "icon/django_boottstrap.html", {"form": form, "menu": menu,
                                                           "wom": Woman.objects.get(pk=11)})


@vary_on_headers("YAryk31")
def send_feedback(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = "crutual message"
            email = form.cleaned_data['email_address']
            body = {
                'username': form.cleaned_data['username'],
                'email': email,
                'message': form.cleaned_data['message'],
            }

            mess = EmailMessage(
                subject=subject,
                body=f"FROM {body['username']} \nMESSAGE:\n{body['message']}\n{body['email']}",
                to=["djangocommunitypython@gmail.com"],
            )
            try:
                mess.attach_file("test.txt")
                mess.send()
            except BadHeaderError:
                return HttpResponse('Error ')
            messages.add_message(request, messages.SUCCESS,
                                     'Thanks for your support, we\'ll work on it ')   
            return redirect("profile")

    form = FeedbackForm()

    return render(request, template_name="icon/send_feedback.html", context={'form': form, "menu": menu})


def setcookie(request):

    # em = EmailMultiAlternatives(subject='Test', body='Test',
    #                             to=['duhanov2003@gmail.com'])
    # em.attach_alternative('<hl>Nice practice to use all of this types</hl>', 'text/html')
    # em.send()
    # return HttpResponseRedirect(reverse("home"))
    pass

@cache_page(60 * 15)
def know_more(request):
    return render(request, "icon/know_more.html", context={"menu" : menu})


class WomanView(APIView):
    """ all news"""
    
    def get(self, request):
        woman = Woman.objects.filter(is_published=True)
        serializer = WomanSerializer(woman, many=True)
        return Response(serializer.data)


class WomanDetailView(APIView):
    """ detail news"""
    
    def get(self, request, pk):
        woman = Woman.objects.get(id=pk, is_published=True)
        serializer = WomanDetailSerializer(woman)
        return Response(serializer.data)


class CategoryView(ModelViewSet):
    """ Category view """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def handle_not_found(request, exception):
    return render(request, "admin/404.html")


def handle_server_error(request):
    return render(request, "admin/500.html")


def handler_forbiden(request, exception):
    return render(request, "icon/403.html")


def handle_url_error(request, exception):
    return render(request, "icon/400.html", status=400)





# class SortPosts(DataMixin, CreateView):

#     model = Woman
#     order = ""


#     def get(self, request, *args, **kwargs):  # get all the consistence of input field
#         self.order = request.GET.get("order", "")
#         order_query = self.order
#         return redirect("home")

    # def get_queryset(self):
    #     if self.order == "most popular down":
    #         print(order_query)
    #         order_query = "-likes"
    #         return order_query
    #     elif self.order == "most popular up":
    #         order_query = "likes"
    #         print(order_query)
    #         return order_query
    #     elif self.order == "most liked up":
    #         order_query = "ip"
    #         print(order_query)
    #         return order_query


# def send_email(request):
#     msg = EmailMessage('Request Callback',
#                        'Here is the new message.', to=['charl@byteorbit.com'])
#     msg.send()
#     return HttpResponseRedirect('/')


# def add_page_model(request):
#   if request.method == "POST":
#       form = NewModelForm(request.POST, request.FILES)
#       if form.is_valid():
#           form.save()
#           return redirect("home")

#   else:
#       form = NewModelForm()
#   return render(request, "icon/add_page_model.html", {"form":form})


# def add_page(request):

#     user_menu = menu.copy()

#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             try:
#                 nane = Woman.objects.create(**form.cleaned_data)
#                 return redirect(nane)
#             except Exception as ex:
#                 form.add_error(None, "Adding post error")
#     else:
#         form = NewsForm()
#     return render(request, "icon/add_page.html", {"form": form, "menu": user_menu})


# @login_required  # allow only for registered members
# def about(request):

#     storage = {
#         "menu": menu
#     }

#     return render(request, 'icon/about.html', context=storage)
