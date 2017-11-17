from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Period, Register, Value2
from django.utils import timezone
import time
from random import randint


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


def modbus(addr, reg, title):
    if title == 'Температура':
        value = addr*5+reg * 30 + randint(1, 4)
    elif title == 'Давление':
        value = addr*4+reg * 2 + randint(1, 3)
    else:
        value = randint(0, 1)
    flag = 'GOOD'
    delay_time = randint(1, 2)
    if delay_time > 18:
        flag = 'TOUT'
    if delay_time > 12:
        flag = 'ERR'
    time.sleep(delay_time)
    return value, flag


@shared_task
def period():
    result = 0
    time_now = timezone.now()
    periods = Period.objects.all()
    registers = None
    for my_period in periods:
        time_delta = timezone.now() - my_period.last_pool_time
        seconds = (my_period.value.hour * 60 + my_period.value.minute) * 60  # + my_period.value.second
        if time_delta.seconds >= seconds:
            my_period.last_pool_time = time_now.replace(second=1)
            registers = Register.objects.filter(enable=True).filter(period=my_period)
            my_period.save()
            # result = result + 1
    if registers is not None:
        for register in registers:
            time_start = timezone.now()
            mr = modbus(register.addr, register.reg, register.title)
            time_delta = (timezone.now() - time_start).seconds
            seconds = (time_start.hour * 60 + time_start.minute) * 60 + time_start.second
            register.last_poll_second = time_delta
            register.save()
            # obj = Value.objects.create(register_id=register.pk, date=time_now, time=seconds, value=mr[0], flag=mr[1])
            # obj.save()
            Value2.add(register=register, date_now=time_start, meaning=mr[0], time_stamp=3)
            result = result + 1
    return result
