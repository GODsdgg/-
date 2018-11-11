from django.shortcuts import render

# Create your views here.



"""
books/ 所有书籍
books/pk/ 获取某一本书籍


areas/infos/        获取省份信息
areas/infos/pk/     市,区县信息


省份信息
select * from tb_areas where parent_id is null;


市的信息
select * from tb_areas where parent_id=110000;
区县
select * from tb_areas where parent_id=110100;



"""

"""
areas/infos/
省的信息 ,获取思路

1. 获取查询结果集
    areas = Areas.objects.filter(parent_id__isnull=True)
2. 将结果给序列化器
    serializer = AreaSerailizer(areas,many=True)
3. 返回响应
    Response(serialzier.data)
"""

"""
areas/infos/pk/
市,区县的信息 ,获取思路

1. 获取查询结果集
    areas = Areas.objects.filter(parent_id=pk)
2. 将结果给序列化器
    serializer = AreaSerailizer(areas,many=True)
3. 返回响应
    Response(serialzier.data)

"""

from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Area
from .serializers import AreaSerailizer,AreaSubSerializer

class AreaViewSet(ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet 最终也是继承自 GenericAPIView

    # ReadOnlyModelViewSet

    # queryset = Area.objects.all()
    # queryset = Area.objects.filter(parent_id__isnull=True)

    def get_queryset(self):

        if self.action == 'list':
            # 获取省的信息
            return Area.objects.filter(parent_id__isnull=True)
        else:
            #获取市区县的信息
            return Area.objects.all()


    # serializer_class = AreaSerailizer

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerailizer
        else:
            return AreaSubSerializer



