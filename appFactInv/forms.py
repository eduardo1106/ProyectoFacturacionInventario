from django import forms
from appFactInv.models import personas,proveedores,telefonos_personas,detalle_productos,productos,colaboradores,sucursales,encabezado_factura,detalle_factura
from django.forms.fields import DateField
from datetime import date, datetime
from django.contrib.admin.widgets import AutocompleteSelect 
from djangoformsetjs.utils import formset_media_js
from django.forms import *

class formpersonas(ModelForm):
    class Meta:
        model = personas
        fields= [
            'nombre_persona',
            'apellido_persona',
            'direccion_persona',
            'nit_persona',
            'telefono_persona',
        ]
        labels ={
            'nombre_persona'   :'Nombres Persona',
            'apellido_persona' :'Apellidos Persona',
            'direccion_persona':'Direccion Persona',
            'nit_persona'      :'Nit Persona',
            'telefono_persona' :'Telefono persona',
            }
        widgets ={
            'nombre_persona':TextInput(attrs={'class':'form-control'}),
            'apellido_persona':TextInput(attrs={'class':'form-control'}),
            'direccion_persona':TextInput(attrs={'class':'form-control'}),
            'nit_persona':TextInput(attrs={'class':'form-control'}),
            'telefono_persona':TextInput(attrs={'class':'form-control'}),
            }



class formproveedores(ModelForm):
    class Meta:
        model= proveedores
        fields= [
            'nombre_proveedor',
            'direccion_proveedor',
            'telefono_proveedor',
            'nit_proveedor',
            'estado',
            'prefijo',
            ]

        labels ={
            'nombre_proveedor':'Nombre del Proveedor',
            'direccion_proveedor':'Dirección Proveedor',
            'telefono_proveedor':'Telefono Proveedor',
            'nit_proveedor':'Nit Proveedor',
            'estado':'Estado',
            'prefijo':'Prefijo',
            }
 
        widgets ={
            'nombre_proveedor':TextInput(attrs={'class':'form-control'}),
            'direccion_proveedor':TextInput(attrs={'class':'form-control'}),
            'telefono_proveedor':TextInput(attrs={'class':'form-control'}),
            'nit_proveedor':TextInput(attrs={'class':'form-control'}),
            'estado':Select(attrs={'class':'form-control'}),
            'prefijo':Select(attrs={'class':'form-control'}),
            }

class formtelefonos_personas(ModelForm):
    class Meta:
        model= telefonos_personas
        fields= [
            'numero_telefono',
            'persona'
            ]
        labels ={
            'numero_telefono':'Numero de Telefono',
            'persona':'Persona',
            }
        widgets ={
            'numero_telefono':TextInput(attrs={'class':'form-control'}),
            'persona':Select(attrs={'class':'form-control'}),
            }

class formdetalle_producto(ModelForm):
    class Meta:
        model = detalle_productos
        fields=[
            'precio_compra',
            'precio_venta',
            'fecha_ingreso',
            'fecha_vencimiento',
            'cantidad_min_stock',
            'estado_producto',
            'descripcion_codigo_lote',
            'proveedor',
            'marca',
            'unidad_medida',
        ]

        labels = {
            'precio_compra':'Precio Compra',
            'precio_venta':'Precio Venta',
            'fecha_ingreso':'Fecha de Ingreso',
            'fecha_vencimiento':'Fecha de Vencimiento',
            'cantidad_min_stock':'Cantidad Min Stock',
            'estado_producto':'Estado Producto',
            'descripcion_codigo_lote':'Codigo Lote',
            'proveedor':'Proveedor',
            'marca':'Marca',
            'unidad_medida':'Unidad de Medida',
             }

        widgets = {
            'precio_compra':NumberInput(attrs={'class':'form-control'}),
            'precio_venta':NumberInput(attrs={'class':'form-control'}),
            'fecha_ingreso':DateInput(attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control datetimepicker-input','id':'fecha_venta','data-target':'#date_joined','data-toggle':'datetimepicke'}),
            'fecha_vencimiento':DateInput(attrs={'class':'form-control','placeholder':'opcional'}),
            'cantidad_min_stock':NumberInput(attrs={'class':'form-control'}),
            'estado_producto':Select(attrs={'class':'form-control'}),
            'descripcion_codigo_lote':TextInput(attrs={'class':'form-control'}),
            'proveedor':Select(attrs={'class':'form-control',}),
            'marca':Select(attrs={'class':'form-control'}),
            'unidad_medida':Select(attrs={'class':'form-control'}),
            } 

class formproducto(ModelForm):
    class Meta:
        model = productos
        fields = [
            'existencia',
            'nombre_producto',
            'descripcion_producto',
            'prefijo',
            ]
        labels = {
            'existencia':'Cantidad',
            'nombre_producto': 'Nombre Producto',
            'descriptcion_producto': 'Descripcion Producto',
            'prefijo': 'Prefijo',
            }
        widgets = {
            'existencia':NumberInput(attrs={'class':'form-control'}) ,
            'nombre_producto':TextInput(attrs={'class':'form-control'}) ,
            'descripcion_producto':TextInput(attrs={'class':'form-control'}) ,
            'prefijo':Select(attrs={'class':'form-control'}),
            }

class formsucursales(ModelForm):
    class Meta:
        model = sucursales 
        fields=[
            'nombre_sucursal',
            'direccion_sucursal',
            'correo_sucursal',
            'nit_sucursal',
            'telefono_sucursal',
            'regimen',
            'prefijo',

        ]
        labels={
            'nombre_sucursal':'Nombre Sucursal',
            'direccion_sucursal':'Direccion Sucursal',
            'correo_sucursal':'Correo Electronico',
            'nit_sucursal':'Numero de Nit',
            'telefono_sucursal':'Telefono',
            'regimen':'Regimen',
            'prefijo': 'Prefijo',
           }
        widgets = {
            'nombre_sucursal':TextInput(attrs={'class':'form-control'}),
            'direccion_sucursal':TextInput(attrs={'class':'form-control'}),
            'correo_sucursal':TextInput(attrs={'class':'form-control'}),
            'nit_sucursal':TextInput(attrs={'class':'form-control'}),
            'telefono_sucursal':TextInput(attrs={'class':'form-control'}),
            'regimen':Select(attrs={'class':'form-control'}),
            'prefijo':Select(attrs={'class':'form-control'}),
            } 

class formcolaboradores(ModelForm):
    class Meta:
        model = colaboradores
        fields=[
            'DPI_Colaborador',
            'correo_colaborador',
            'estado_colaborador',
            'prefijo',
            'perfil_colaborador',
        ]
        labels={
            'DPI_Colaborador':'DPI Colaborador',
            'correo_colaborador':'Correo Electronico',
            'estado_colaborador': 'Estado',
            'prefijo':'Prefijo',
            'perfil_colaborador':'Perfil Colaborador',
        }
        widgets = {
            'DPI_Colaborador':TextInput(attrs={'class':'form-control'}),
            'correo_colaborador':TextInput(attrs={'class':'form-control'}),
            'estado_colaborador':Select(attrs={'class':'form-control'}),
            'prefijo':Select(attrs={'class':'form-control'}),
            'perfil_colaborador':Select(attrs={'class':'form-control'}),
            } 

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = encabezado_factura
        fields = '__all__'
        widgets = {
            'cliente': Select(attrs={'class': 'form-control','style': 'width: 100%'}),
            'fecha_venta':DateInput(format='%Y-%m-%d',
                attrs={
                    'value':datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }),
            'sucursal':Select(attrs={'class': 'form-control','style': 'width: 100%'}),
            'colaborador':Select(attrs={'class': 'form-control','style': 'width: 100%'}),  
             'iva': TextInput(attrs={'class': 'form-control',}),
             'subtotal': TextInput(attrs={'readonly': True,'class': 'form-control',}),
             'total': TextInput(attrs={'readonly': True,'class': 'form-control',})
        }

class formlogin(ModelForm):
    class Meta:
      
        widgets ={
            'username':TextInput(attrs={'class':'form-control','type':'text','placeholder':'Ingrese su usuario', 'name':'username'}),
            'password':TextInput(attrs={'class':'form-control','type':'password','placeholder':'Ingrese su contraseña', 'name':'password'}),
            }