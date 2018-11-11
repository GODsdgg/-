from django.conf.urls import url

from  . import views

urlpatterns = [


]

# 视图集的url是自动生成的
from rest_framework.routers import DefaultRouter

# 1.创建router
router = DefaultRouter()

# areas/infos/        获取省份信息
# areas/infos/pk/     市,区县信息
# 2.设置url
router.register(r'infos',views.AreaViewSet,base_name='')

# 3.需要把生成的url添加到 urlpatterns
urlpatterns += router.urls

