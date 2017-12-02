import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse  # HttpResponse,
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.utils import timezone
from .serializers import DeviceSerializer, RegisterSerializer, ValueSerializer, Value2Serializer, \
    ValueInRegSerializer, ValueInDevSerializer, TimeStampSerializer
from rest_framework.views import APIView
from rest_framework import generics
from .models import Device, Register, Value2, TimeStamp


# Create your views here.
def mb_list(request):
    regs = Register.objects.all()
    devices = Device.objects.all()
    value2s = Value2.objects.all()
    # Value2.add(register=1, meaning=123, time_stamp=3)
    return render(request, 'mb_server/mb_list.html', {'devices': devices, 'regs': regs})


def mb_detals(request, pk):
    # devices = get_object_or_404(Device, pk=pk)
    device = Device.objects.get(pk=pk)
    regs = Register.objects.all()
    # Value2.add(register=1, meaning=123, time_stamp=3)
    return render(request, 'mb_server/mb_delail.html', {'device': device, 'regs': regs, 'device_id': pk})


# def docx_all(request):
#     memos = Register.objects.all()  # .order_by('number').reverse()
#     return render(request, 'docx/docx_all2.html', {'memos': memos})


# @csrf_exempt
# def mb_json(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         values = Value.objects.all()  # 11- статус в работе, костыль
#         serializer = ValueSerializer(values, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ValueSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# @api_view(['GET', 'POST'])
# def mb_json2(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         values = Value2.objects.all()  # 11- статус в работе, костыль
#         serializer = Value2Serializer(values, many=True)
#         # r = [{'data1': ['1', '20', '30'], 'data2': ['1', '5', '4']}]
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = Value2Serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def mb_detail_json2(request, pk):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     try:
#         snippet = Value2.objects.get(pk=pk)
#     except Value2.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = Value2Serializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = Value2Serializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class MbJsonList(generics.ListCreateAPIView):
    queryset = Value2.objects.all()
    serializer_class = Value2Serializer


class MbJsonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Value2.objects.all()
    serializer_class = Value2Serializer


class MbJsonListDevice(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class MbJsonDetailDevice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class MbJsonListTimeStamp(generics.ListCreateAPIView):
    queryset = TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


class MbJsonDetailTimeStamp(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeStamp.objects.all()
    serializer_class = TimeStampSerializer


# --------------------------------------------------
class JsonDeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class JsonDeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class JsonRegisterList(generics.ListCreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


class JsonRegisterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    # class JsonValueList(generics.ListCreateAPIView):
    #     queryset = Value2.objects.all()
    #     serializer_class = ValueSerializer


# --------------- Val ----------------------------- #
class JsonValueList(generics.ListCreateAPIView):
    # queryset = Value2.objects.all()
    serializer_class = ValueSerializer

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        else:
            date_now = datetime.datetime.strptime(his_date, '%y%m%d')
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        return queryset


class JsonValueDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Value2.objects.all()
    serializer_class = ValueSerializer

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        else:
            date_now = datetime.datetime.strptime(his_date, '%y%m%d')
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        return queryset


# --------------- Val End ------------------------- #

# --------------- Reg ----------------------------- #
class JsonValueInRegList(generics.ListCreateAPIView):
    # queryset = Value2.objects.all()
    serializer_class = ValueInRegSerializer

    # lookup_fields = 'register__id'

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        else:
            his_date = datetime.datetime.strptime(his_date, '%y%m%d')
            queryset = Value2.objects.filter(date__date=his_date)
        return queryset


class JsonValueInRegDetail(generics.ListCreateAPIView):
    # queryset = Register.objects.all()
    serializer_class = ValueInRegSerializer

    # lookup_fields = 'register__id'

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        reg_id = self.kwargs.get('reg_pk', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            if reg_id is None:
                queryset = Value2.objects.filter(date__date=date_now)
            else:
                queryset = Value2.objects.filter(date__date=date_now, register_id=reg_id)
        else:
            his_date = datetime.datetime.strptime(his_date, '%y%m%d')
            if reg_id is None:
                queryset = Value2.objects.filter(date__date=his_date)
            else:
                queryset = Value2.objects.filter(date__date=his_date, register_id=reg_id)
        return queryset


# --------------- Reg End ------------------------- #

# --------------- Dev ----------------------------- #
class JsonValueInDevList(generics.ListCreateAPIView):
    # queryset = Device.objects.all()
    serializer_class = ValueInDevSerializer

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = Value2.objects.filter(date__date=date_now)
        else:
            his_date = datetime.datetime.strptime(his_date, '%y%m%d')
            queryset = Value2.objects.filter(date__date=his_date)
        return queryset


class JsonValueInDevDetail(generics.ListCreateAPIView):
    # queryset = Device.objects.all()
    serializer_class = ValueInDevSerializer

    def get_queryset(self):
        his_date = self.kwargs.get('date', None)
        dev_id = self.kwargs.get('dev_pk', None)
        if his_date is None:
            date_now = timezone.now()
            date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
            if dev_id is None:
                queryset = Value2.objects.filter(date__date=date_now)
            else:
                queryset = Value2.objects.filter(date__date=date_now, register__device_id=dev_id)
        else:
            his_date = datetime.datetime.strptime(his_date, '%y%m%d')
            if dev_id is None:
                queryset = Value2.objects.filter(date__date=his_date)
            else:
                queryset = Value2.objects.filter(date__date=his_date, register__device_id=dev_id)
        return queryset

# --------------- Dev End ------------------------- #
#
# class MbJsonListTimeStamp(generics.ListCreateAPIView):
#     queryset = TimeStamp.objects.all()
#     serializer_class = TimeStampSerializer
#
#
# class MbJsonDetailTimeStamp(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TimeStamp.objects.all()
#     serializer_class = TimeStampSerializer
