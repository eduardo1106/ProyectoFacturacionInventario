from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.forms import model_to_dict



status=[
(1,'Activo'),
(0,'Inactivo'),
]

class prefijos(models.Model):
    descripcion_prefijo=models.CharField(max_length=5)
    def __str__(self):
        return self.descripcion_prefijo

class personas(models.Model):
    nombre_persona=models.CharField(max_length=60)
    apellido_persona=models.CharField(max_length=60)
    direccion_persona=models.TextField()
    nit_persona=models.CharField(null=True, max_length=10, unique=True)
    telefono_persona=models.CharField(null=True,blank=True, max_length=8)
    def __str__(self):
        return self.nombre_persona 

    def toJSON(self):
        item = model_to_dict(self)
        return item


    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['id']



   
class proveedores(models.Model):
    nombre_proveedor=models.CharField(max_length=60)
    direccion_proveedor=models.TextField()
    telefono_proveedor=models.CharField(max_length=8)
    nit_proveedor=models.CharField( max_length=10,unique=True)
    prefijo=models.ForeignKey(prefijos,on_delete=models.CASCADE)
    estado=models.IntegerField(null=False,blank=False,choices=status,default=1)
    persona_contacto=models.ForeignKey(personas,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_proveedor



class telefonos_personas (models.Model):
    numero_telefono=models.CharField(max_length=8)
    persona=models.ForeignKey(personas,on_delete=models.CASCADE)

class marcas(models.Model):
    descripcion_marca=models.CharField(max_length=20)
    categoria=models.CharField(max_length=1)
    def __str__(self):
        return self.descripcion_marca


class unidad_medidas(models.Model):
    descripcion_unidad_medida=models.CharField(max_length=20)
    def __str__(self):
        return self.descripcion_unidad_medida


class detalle_productos(models.Model):
    precio_venta=models.DecimalField(max_digits=6,decimal_places=2)
    precio_compra=models.DecimalField(max_digits=6,decimal_places=2)
    fecha_ingreso=models.DateField(default=datetime.now)
    fecha_vencimiento=models.DateField(null=True,blank=True)
    cantidad_min_stock=models.PositiveIntegerField()
    estado_producto=models.IntegerField(null=False,blank=False,choices=status,default=1)
    descripcion_codigo_lote=models.CharField(max_length=30)
    proveedor=models.ForeignKey(proveedores,on_delete=models.CASCADE)
    marca=models.ForeignKey(marcas,null=True,on_delete=models.CASCADE)
    unidad_medida=models.ForeignKey(unidad_medidas,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.precio_venta)

    def toJSON(self):
        item = model_to_dict(self)
        return item    


class productos(models.Model):
    existencia=models.PositiveIntegerField()
    nombre_producto=models.TextField()
    descripcion_producto=models.TextField()
    prefijo=models.ForeignKey(prefijos,null=True,blank=True,on_delete=models.CASCADE)
    detalle_producto=models.ForeignKey(detalle_productos,on_delete=models.CASCADE)
    def __str__(self):
        return self.descripcion_producto

    def toJSON(self):
        item = model_to_dict(self)
        item['detalle_producto'] = self.detalle_producto.toJSON()
        item['existencia'] = format(self.existencia, '.2f')
        return item

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['id']

     

class regimens(models.Model):
    descripcion_regimen=models.CharField(max_length=20)
    impuesto_regimen=models.PositiveIntegerField()
    def __str__(self):
        return self.descripcion_regimen


class sucursales(models.Model):
    nombre_sucursal=models.CharField(max_length=40)
    direccion_sucursal=models.TextField()
    correo_sucursal=models.CharField(max_length=50)
    nit_sucursal=models.CharField(max_length=10, unique=True)
    telefono_sucursal=models.CharField(max_length=10)
    regimen=models.ForeignKey(regimens,on_delete=models.CASCADE)
    prefijo=models.ForeignKey(prefijos,on_delete=models.CASCADE)
    persona_encargada=models.ForeignKey(personas,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_sucursal

class perfiles_colaboradores(models.Model):
    nombre_perfil=models.CharField(max_length=20)
    descripcion_perfil=models.CharField(max_length=40)
    def __str__(self):
        return self.nombre_perfil


class colaboradores(models.Model):
    DPI_Colaborador=models.CharField(max_length=16)
    correo_colaborador=models.CharField(max_length=50)
    estado_colaborador=models.IntegerField(null=False,blank=False,choices=status,default=1)
    prefijo=models.ForeignKey(prefijos,on_delete=models.CASCADE)
    perfil_colaborador=models.ForeignKey(perfiles_colaboradores,on_delete=models.CASCADE)
    persona=models.ForeignKey(personas,on_delete=models.CASCADE)
    def __str__(self):
        return '%s %s' % (self.persona.nombre_persona, self.persona.apellido_persona)


class encabezado_factura(models.Model):
    
    cliente=models.ForeignKey(personas,on_delete=models.CASCADE)
    fecha_venta=models.DateField(default=datetime.now)
    sucursal=models.ForeignKey(sucursales,on_delete=models.CASCADE)
    colaborador=models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    subtotal= models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.cliente.nombre_persona

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['colaborador'] = self.colaborador.toJSON()
        item['sucursal'] = self.sucursal.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_venta'] = self.fecha_venta.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class detalle_factura(models.Model):
    venta=models.ForeignKey(encabezado_factura, on_delete=models.CASCADE)
    producto=models.ForeignKey(productos,on_delete=models.CASCADE)
    precio=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad=models.IntegerField(default=0)
    subtotal=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    def __str__(self):
        return self.producto.descripcion_producto


    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cantidad'] = format(self.cantidad, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
    

        
        





