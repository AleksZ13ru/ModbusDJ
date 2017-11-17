from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json

DB_DATETIME_FORMAT = '%d/%b/%Y %H:%M:%S'
DB_DATE_FORMAT = '%m/%d/%Y'
DB_DATETIME_Z_FORMAT = '%m/%d/%Y 0:0'
DB_TIME_FORMAT = "%H:%M"


class Port(models.Model):
    class Meta:
        verbose_name = "Порт"
        verbose_name_plural = "Порты"

    name = models.CharField(max_length=10)  # имя порта

    def __str__(self):
        return self.name


class Period(models.Model):
    class Meta:
        verbose_name = "Период"
        verbose_name_plural = "Периоды"

    value = models.TimeField()  # заданное время
    last_pool_time = models.DateTimeField()  # время последнего опроса

    def __str__(self):
        result = 'Период: %s -  Последнее обновление: %s' % (
            self.value.second,
            self.last_pool_time.strftime(DB_DATETIME_FORMAT)
        )
        return result


class Device(models.Model):
    class Meta:
        verbose_name = "Устройство"
        verbose_name_plural = "Устройства"

    title = models.TextField()  # имя объекта(название группы регистров - пример=битумный котел)

    def __str__(self):
        return self.title


class Register(models.Model):
    class Meta:
        verbose_name = "Регистер"
        verbose_name_plural = "Регистры"

    enable = models.BooleanField(default=False)  # разрешен опрос
    port = models.ForeignKey('Port')  # порт для работы
    device = models.ForeignKey('Device', blank=True, null=True,
                               related_name='registers')  # устройство(идентификатор место расположения)
    title = models.TextField(blank=True, null=True)  # название для отображения - пример=температура, давление
    addr = models.IntegerField()  # адрес устройства
    reg = models.IntegerField()  # номер регистра
    period = models.ForeignKey('Period')  # период опроса
    valid = models.IntegerField(blank=True, null=True)  # процент успешности 20 запросов
    last_poll_second = models.IntegerField(blank=True, null=True)  # количество секунд затраченное на послений опрос
    counter_error = models.IntegerField(blank=True, null=True)  # число ошибок чтения
    last_value = models.IntegerField(blank=True, null=True)  # последнее значение
    last_time = models.DateTimeField(blank=True, null=True)  # время заполнения last_value

    @staticmethod
    def last_update(register, time=None, value=None):
        obj = Register.objects.get(id=register)
        obj.last_time = time
        obj.last_value = value
        obj.save()

    def __str__(self):
        result = '%s: %s (%d:%d)' % (
            self.device,
            self.title,
            self.addr,
            self.reg
        )
        return result

        # def __unicode__(self):
        #     return '%s' % self.title


class ValueFlag(models.Model):
    class Meta:
        verbose_name = "Статус флага результата"
        verbose_name_plural = "Статусы флага результата"

    # -good - опрос состоялся
    # -time_out - опроса не было, не хватило времени
    # -fault - опрос состоялся, данные не верны
    title = models.CharField(max_length=10)  # название статуса
    comment = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Value(models.Model):
    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"

    FLAG_STAT = (
        ('GOOD', 'Good'),
        ('TOUT', 'Time Out'),
        ('ERR', 'Error')
    )
    register = models.ForeignKey('Register')  # id
    date = models.DateField()  # дата опроса
    time = models.IntegerField()  # время опроса(номер секунды)
    value = models.IntegerField()  # значение
    flag = models.CharField(max_length=4, choices=FLAG_STAT)  # флаг состояния последнего опроса

    def __str__(self):
        result = '%s %s | %s=%d | %s' % (
            self.date,
            self.time,
            self.register,
            self.value,
            self.flag
        )
        return result


class Date(models.Model):
    class Meta:
        verbose_name = "Дата"
        verbose_name_plural = "Даты"

    date = models.DateTimeField()

    def __str__(self):
        # result = '%s' % (
        #     self.date
        # )
        return self.date.strftime(DB_DATETIME_FORMAT)


class TimeStamp(models.Model):
    class Meta:
        verbose_name = "Штамп времени"
        verbose_name_plural = "Штампы времени"

    title = models.CharField(max_length=40)
    x = JSONField()

    def __str__(self):
        return self.title


class Value2(models.Model):
    class Meta:
        verbose_name = "Значение2"
        verbose_name_plural = "Значения2"

    FLAG_STAT = (
        ('GOOD', 'Good'),
        ('TOUT', 'Time Out'),
        ('ERR', 'Error')
    )
    register = models.ForeignKey('Register', related_name='values')
    date = models.ForeignKey('Date')
    flag = models.CharField(max_length=4, choices=FLAG_STAT)  # флаг состояния цепочки данных
    time_stamp = models.ForeignKey('TimeStamp')
    # error_list = JSONField()
    value = JSONField()

    def __str__(self):
        result = '%s | %s=%d | %s' % (
            self.date,
            self.register,
            len(self.value),
            self.flag
        )
        return result

    # meaning=смысл, значение, важность
    @staticmethod
    def add(register=None, date_now=timezone.now(), flag=FLAG_STAT[0][0], time_stamp=None, meaning=None):
        current_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
        obj_data = Date.objects.get_or_create(date=current_date)[0]
        current_time = date_now.time()
        total_minute = (current_time.hour * 60 + current_time.minute)
        try:
            obj = Value2.objects.filter(register_id=register.pk, date_id=obj_data.id).get()
            #  есть строка в базе
            lvalue = obj.value
            if len(lvalue) < total_minute - 1:
                for i in range(total_minute - len(lvalue)):
                    lvalue.append(0)
            lvalue.append(meaning)
            obj.value = lvalue
            obj.save()

        except ObjectDoesNotExist:
            lvalue = []
            for i in range(total_minute - 1):
                lvalue.append(0)
            lvalue.append(meaning)
            obj = Value2.objects.create(register_id=register.pk, date_id=obj_data.id, flag='GOOD',
                                        time_stamp_id=time_stamp, value=lvalue)
            obj.save()

        Register.last_update(register=register.pk, time=date_now, value=meaning)
