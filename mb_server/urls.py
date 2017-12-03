from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.mb_list, name='mb_list'),
    url(r'^his/(?P<date>[0-9]+)$', views.mb_his, name='mb_his'),
    url(r'^(?P<pk>[0-9]+)$', views.mb_detals, name='mb_detals'),
    # url(r'^all/$', views.mb_all, name='mb_all'),
    # url(r'^json/$', views.mb_json, name='mb_json'),

    url(r'^json2/$', views.MbJsonList.as_view(), name='mb_json2'),
    url(r'^json2/(?P<pk>[0-9]+)$', views.MbJsonDetail.as_view(), name='mb_json2_detail'),

    url(r'^json2dev/$', views.MbJsonListDevice.as_view(), name='mb_json2_dev'),
    url(r'^json2dev/(?P<pk>[0-9]+)$', views.MbJsonDetailDevice.as_view(), name='mb_json2_dev_detail'),

    url(r'^json2/timestamp/$', views.MbJsonListTimeStamp.as_view(), name='mb_json2_time_stamp'),
    url(r'^json2/timestamp/(?P<pk>[0-9]+)$', views.MbJsonDetailTimeStamp.as_view(), name='mb_json2_time_stamp_detail'),
    # url(r'^json/(?P<pk>[0-9]+)/$', views.docx_json_detail, name='mb_json_detail'),

    url(r'^json/dev/$', views.JsonDeviceList.as_view(), name='json_dev'),
    url(r'^json/dev/(?P<pk>[0-9]+)$', views.JsonDeviceDetail.as_view(), name='json_dev_detail'),

    url(r'^json/reg/$', views.JsonRegisterList.as_view(), name='json_reg'),
    url(r'^json/reg/(?P<pk>[0-9]+)$', views.JsonRegisterDetail.as_view(), name='json_reg_detail'),

    url(r'^json/val/$', views.JsonValueList.as_view(), name='json_val'),
    url(r'^json/val/(?P<pk>[0-9]+)$', views.JsonValueDetail.as_view(), name='json_val_detail'),

    url(r'^json/his/(?P<date>[0-9]+)/val/$', views.JsonValueList.as_view(), name='json_his_val'),
    url(r'^json/his/(?P<date>[0-9]+)/val/(?P<pk>[0-9]+)$', views.JsonValueDetail.as_view(), name='json_his_val_detail'),

    url(r'^json/val_in_reg/$', views.JsonValueInRegList.as_view(), name='json_val_in_reg'),
    url(r'^json/val_in_reg/(?P<reg_pk>[0-9]+)$', views.JsonValueInRegDetail.as_view(), name='json_val_in_reg_detail'),

    url(r'^json/his/(?P<date>[0-9]+)/val_in_reg/$', views.JsonValueInRegList.as_view(), name='json_his_val_in_reg'),
    url(r'^json/his/(?P<date>[0-9]+)/val_in_reg/(?P<reg_pk>[0-9]+)$', views.JsonValueInRegDetail.as_view(),
        name='json_his_val_in_reg_detail'),

    url(r'^json/val_in_dev/$', views.JsonValueInDevList.as_view(), name='json_val_in_dev'),
    url(r'^json/val_in_dev/(?P<dev_pk>[0-9]+)$', views.JsonValueInDevDetail.as_view(), name='json_val_in_dev_detail'),

    url(r'^json/his/(?P<date>[0-9]+)/val_in_dev/$', views.JsonValueInDevList.as_view(), name='json_his_val_in_dev'),
    url(r'^json/his/(?P<date>[0-9]+)/val_in_dev/(?P<dev_pk>[0-9]+)$', views.JsonValueInDevDetail.as_view(),
        name='json_his_val_in_dev_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
