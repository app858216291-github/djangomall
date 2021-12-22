from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
# Create your views here.
from DJMall.utils.views import DJMallBaseView
from dadmin.forms import DJMallAuthenticationForm
from users.forms import DJMallRegisterForm

User = get_user_model()


class DJMallAuthBackend(ModelBackend):
    """ 自定义用户验证，继承ModelBackend, 重写authenticate方法
    ModelBackend 类实际是django继承BaseBackend实现的验证登录后端，
    我们这里使用的是django自带的验证后端，那最好的做法就是扩展重写该类
    """
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class DJMallLoginView(DJMallBaseView, LoginView):
    # 登录页面
    form_class = DJMallAuthenticationForm
    template_name = 'users/login.html'
    next_page = '/'
    extra_context = {
        'title': '登录',
        'sub_title': 'DJMall商城系统！'
    }
    

class DJMallRegisterView(DJMallBaseView, TemplateView):
    # 注册视图
    template_name = 'users/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DJMallRegisterForm()
        return context
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

