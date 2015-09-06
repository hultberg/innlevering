from django.contrib import admin
from .models import Compo, Bidrag, BidragFile

# Register your models here.
admin.site.register(Compo)
admin.site.register(Bidrag)
admin.site.register(BidragFile)
