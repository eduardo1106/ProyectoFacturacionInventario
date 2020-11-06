import json
from django.http import HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from appFactInv.models import encabezado_factura,personas,proveedores,telefonos_personas,productos,detalle_productos,colaboradores,sucursales,detalle_factura
from appFactInv.forms import formproveedores,formpersonas,formtelefonos_personas,formproducto,formdetalle_producto,formcolaboradores,formsucursales,SaleForm
from django.shortcuts import render,redirect
from django.db.models import Q
from datetime import date
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def Index(request):
    return render (request,"index.html")

    
def BuscarClientes(request):
    busqueda= request.GET.get("buscar")
    persona= personas.objects.get(pk=1).only('id','nombre_persona','apellido_persona')
    if busqueda:
        persona=personas.objects.filter(
        Q(nombre_persona__icontains=busqueda)
        ).distinct()
    return render (request,"BuscarClientes.html",{"persona":persona})


def BuscarProveedores(request):
    busqueda= request.GET.get("buscar")
    proveedor= proveedores.objects.all()
    if busqueda:
        proveedor=proveedores.objects.filter(
            Q(nombre_proveedor__icontains=busqueda)|
            Q(direccion_proveedor__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProveedores.html",{"proveedor":proveedor})

def BuscarProveedoresDelete(request):
    busqueda= request.GET.get("buscar")
    proveedor= proveedores.objects.all()
    if busqueda:
        proveedor=proveedores.objects.filter(
            Q(nombre_proveedor__icontains=busqueda)|
            Q(direccion_proveedor__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProveedoresDelete.html",{"proveedor":proveedor})


def BuscarColaboradores(request):
    busqueda= request.GET.get("buscar")
    colaborador= colaboradores.objects.all()

    if busqueda:
        colaborador=colaboradores.objects.filter(
            Q(nombre_persona__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarColaboradores.html",{"colaborador":colaborador})


def BuscarProductos(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(nombre_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductos.html",{"producto":producto})

def BuscarProductosDelete(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(nombre_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductosDelete.html",{"producto":producto})


class CrearProductos(CreateView):
    model = productos
    template_name='CrearProductos.html'
    form_class = formproducto
    second_form_class = formdetalle_producto
    success_url='/crear_productos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearProductos, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproducto = form.save(commit=False)
            guardarproducto.detalle_producto = form2.save()
            guardarproducto.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class EditarProductos(UpdateView):
    model=productos
    second_model=detalle_productos
    template_name='EditarProductos.html'
    form_class = formproducto 
    second_form_class= formdetalle_producto
    success_url='/buscar_productos'
    
    def get_context_data(self,**kwargs):
        context= super(EditarProductos,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        productos=self.model.objects.get(id=pk)
        detalle_productos=self.second_model.objects.get(id=productos.detalle_producto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=detalle_productos)
        context['id']=pk
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_producto = kwargs['pk']
        productos = self.model.objects.get(id=id_producto)
        detalle_productos = self.second_model.objects.get(id=productos.detalle_producto_id)
        form = self.form_class(request.POST, instance=productos)
        form2 = self.second_form_class(request.POST,instance=detalle_productos)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class DeleteProducto(DeleteView):
    model=productos
    template_name='MensajeBorrarProductos.html'
    success_url='/buscar_productos_delete'



class CrearSucursales(CreateView):
    model = sucursales
    template_name='CrearSucursales.html'
    form_class = formsucursales
    second_form_class = formpersonas
    success_url='/crear_sucursales'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object
   
    def get_context_data(self, **kwargs):
        contex = super(CrearSucursales, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarsucursal = form.save(commit=False)
            guardarsucursal.persona_encargada = form2.save()
            guardarsucursal.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class CrearProveedores(CreateView):
    model = proveedores
    template_name='CrearProveedores.html'
    form_class = formproveedores
    second_form_class = formpersonas
    success_url='/crear_proveedores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object
   
    def get_context_data(self, **kwargs):
        contex = super(CrearProveedores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproveedor = form.save(commit=False)
            guardarproveedor.persona_contacto = form2.save()
            guardarproveedor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class EditarProveedores(UpdateView):
    model=proveedores
    second_model=personas
    template_name='EditarProveedores.html'
    form_class = formproveedores 
    second_form_class= formpersonas
    success_url='/buscar_proveedores'
    
    def get_context_data(self,**kwargs):
        context= super(EditarProveedores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        proveedores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=proveedores.persona_contacto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_proveedor = kwargs['pk']
        proveedores = self.model.objects.get(id=id_proveedor)
        personas = self.second_model.objects.get(id=proveedores.persona_contacto_id)
        form = self.form_class(request.POST, instance=proveedores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())
      
class DeleteProveedores(DeleteView):
    model=proveedores
    template_name='MensajeBorrarProveedores.html'
    success_url='/buscar_productos_delete' 


class CrearClientes(CreateView):
    model = personas
    template_name='CrearClientes.html'
    form_class = formpersonas
    success_url='/crear_clientes'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object
   
    def get_context_data(self, **kwargs):
        contex = super(CrearClientes, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
            return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        
        if form.is_valid():
            guardarcliente = form.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))


class CrearColaboradores(CreateView):
    model = colaboradores
    template_name='CrearColaboradores.html'
    form_class = formcolaboradores
    second_form_class = formpersonas
    success_url='/crear_colaboradores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex =super(CrearColaboradores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarcolab = form.save(commit=False)
            guardarcolab.persona = form2.save()
            guardarcolab.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class EditarColaboradores(UpdateView):
    model=colaboradores
    second_model=personas
    template_name='EditarColaboradores.html'
    form_class = formcolaboradores 
    second_form_class= formpersonas
    success_url='/buscar_colaboradores'

    def get_context_data(self,**kwargs):
        context= super(EditarColaboradores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        colaboradores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=colaboradores.persona_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_colaborador = kwargs['pk']
        colaboradores = self.model.objects.get(id=id_colaborador)
        personas = self.second_model.objects.get(id=colaboradores.persona_id)
        form = self.form_class(request.POST, instance=colaboradores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class CrearTelefonosPersonas(CreateView):
    model = telefonos_personas
    template_name='CrearTelefonosPersonas.html'
    form_class = formtelefonos_personas
    success_url='/crear_telefonos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object
   
    def get_context_data(self, **kwargs):
        contex = super(CrearTelefonosPersonas, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)
        return contex  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
     
    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            guardartelefono = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))


class SaleCreateView(CreateView):
    model = encabezado_factura
    form_class = SaleForm
    template_name = 'Facturacion.html'
    success_url = reverse_lazy('crear_facturas')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = productos.objects.filter(descripcion_producto__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.descripcion_producto
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                
                    sale = encabezado_factura()
                    sale.fecha_venta = vents['fecha_venta']
                    sale.cliente_id = vents['cliente']
                    sale.colaborador_id=vents['colaborador']
                    sale.sucursal_id=vents['sucursal']
                    sale.subtotal = float(vents['subtotal'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = detalle_factura()
                        det.venta_id = sale.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.detalle_producto.precio_venta = float(i['detalle_producto.precio_venta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
           
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context