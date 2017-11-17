from django.contrib import admin
from .models import Port, Period, Register, Device
from .models import Value2, Date, TimeStamp


admin.site.register(Port)
admin.site.register(Register)
admin.site.register(Device)
admin.site.register(Value2)
admin.site.register(Date)
admin.site.register(TimeStamp)
admin.site.register(Period)
