from django.contrib import admin
from appFactInv.models import personas,prefijos,proveedores,telefonos_personas,detalle_productos,productos,encabezado_factura,detalle_factura

from django.forms import TextInput, Textarea 
from django.db import models 

admin.site.register(personas)
admin.site.register(prefijos)
admin.site.register(proveedores)
admin.site.register(telefonos_personas)
admin.site.register(detalle_productos)
admin.site.register(productos)
admin.site.register(encabezado_factura)
admin.site.register(detalle_factura)


class YourModelAdmin(admin.ModelAdmin): 
 formfield_overrides = { 
  models.CharField: {'widget': TextInput(attrs={'size':'20'})}, 
  models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}, 
 } 
