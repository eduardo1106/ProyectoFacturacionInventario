
from django.contrib import admin
from django.urls import path
from appFactInv.views import Index,CrearProveedores,EditarProveedores,BuscarProveedores,CrearClientes,CrearTelefonosPersonas,CrearProductos,EditarProductos,BuscarProductos,BuscarProductosDelete,DeleteProducto,CrearColaboradores,BuscarColaboradores,EditarColaboradores,CrearSucursales,DeleteProveedores,BuscarProveedoresDelete,SaleCreateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView

urlpatterns=[
    path('index/',Index, name="Index"),
    
    path('crear_proveedores/',CrearProveedores.as_view(),name="crear_proveedores"),
    path('buscar_proveedores/',BuscarProveedores,name="buscar_proveedores"),
    path('editar_proveedores/<int:pk>',EditarProveedores.as_view(), name="editar_proveedores"),
    path('buscar_proveedores_delete/',BuscarProveedoresDelete,name="buscar_proveedores_delete"),
    path('borrar_proveedores/<int:pk>/',DeleteProveedores.as_view(), name="borrar_proveedores"),
    
    path('crear_clientes/',CrearClientes.as_view(),name="crear_clientes"),
   # path('buscar_clientes/',BuscarClientes,name="buscar_clientes"),
   # path('editar_clientes/<int:pk>',EditarClientes.as_view(), name="editar_clientes"),
    
    path('crear_productos/',CrearProductos.as_view(),name="crear_productos"),
    path('buscar_productos/',BuscarProductos,name="buscar_productos"),
    path('editar_productos/<int:pk>',EditarProductos.as_view(), name="editar_productos"),
    path('buscar_productos_delete/',BuscarProductosDelete,name="buscar_productos_delete"),
    path('borrar_productos/<int:pk>/',DeleteProducto.as_view(), name="borrar_productos"),
    
    path('crear_colaboradores/',CrearColaboradores.as_view(),name="crear_colaboradores"),
    path('buscar_colaboradores/',BuscarColaboradores,name="buscar_colaboradores"),
    path('editar_colaboradores/<int:pk>/',EditarColaboradores.as_view(),name="editar_colaboradores"),
    
    path('crear_sucursales/',CrearSucursales.as_view(),name="crear_sucursales"),
   
    path('agregar_telefonos/',CrearTelefonosPersonas.as_view(),name="agregar_telefono"),
    path('crear_facturas/',SaleCreateView.as_view(),name="crear_facturas"),
    path('',LoginView.as_view(template_name='login.html'),name='login'), 
    ] +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)