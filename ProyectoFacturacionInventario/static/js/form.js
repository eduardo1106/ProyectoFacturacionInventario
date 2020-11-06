var tblProducts;
var vents = {
    items: {
        cliente: '',
        fecha_venta: '',
        sucursal:'',
        colaborador:'',
        subtotal:'0.00',
        total: '0.00',
        products: []
    },
    calcular_factura: function () {
        var subtotal = 0.00;
        $.each(this.items.products, function (pos,dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.detalle_producto.precio_venta);
            subtotal+=dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.total = this.items.subtotal ;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
        
    },
    list: function () {
        this.calcular_factura();    
    tblProducts =$('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "cantidad"},
                {"data": "descripcion_producto"},
                {"data": "detalle_producto.precio_venta"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Q' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Q' + parseFloat(data).toFixed(2);
                    }
                },
      
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]');

            },


            initComplete: function (settings, json) {

            }
        });
  /*      $("input[name='iva']").TouchSpin({
            min: 0,
            max: 100,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            postfix: '%'
        }).on('change',function () {
            vents.calcular_factura();
        })
        .val(0.12);
    
   */ 
    
    
    
    
    
    },
};

$(function () {

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });
  // evento cantidad 
  $('#tblProducts tbody')
  .on('click','a[rel="remove"]',function(){
    var tr = tblProducts.cell($(this).closest('td, li')).index();
    vents.items.products.splice(tr.row,1);
    vents.list();
  
  })  
  .on('change','input[name="cant"]', function () {
    console.clear();
    var cant = parseInt($(this).val());
    var tr = tblProducts.cell($(this).closest('td, li')).index();
    vents.items.products[tr.row].cantidad = cant;
    vents.calcular_factura();
    $('td:eq(4)', tblProducts.row(tr.row).node()).html('Q' + vents.items.products[tr.row].subtotal.toFixed(2));

});

$('form').on('submit',function (e) {
    e.preventDefault();

    if(vents.items.products.length === 0){
        message_error('Debe al menos tener un item en su detalle de venta');
        return false;
    }

    vents.items.fecha_venta = $('input[name="fecha_venta"]').val();
    vents.items.cliente = $('select[name="cliente"]').val();
    vents.items.colaborador = $('select[name="colaborador"]').val();
    vents.items.sucursal = $('select[name="sucursal"]').val();
    var parameters = new FormData();
    parameters.append('action', $('input[name="action"]').val());
    parameters.append('vents', JSON.stringify(vents.items));
    submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/crear_facturas';
        });
  


      
   
});

vents.list();



function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
    theme: 'material',
    title: title,
    icon: 'fa fa-info',
    content: content,
    columnClass: 'small',
    typeAnimated: true,
    cancelButtonClass: 'btn-primary',
    draggable: true,
    dragWindowBorder: false,
    buttons: {
        info: {
            text: "Si",
            btnClass: 'btn-primary',
            action: function () {
                $.ajax({
                    url: url, //window.location.pathname
                    type: 'POST',
                    data: parameters,
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                }).done(function (data) {
                  

                    console.log(data);


                    if (!data.hasOwnProperty('error')) {
                        callback();
                        return false;
                    }
                    
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {

                });
            }
        },
        danger: {
            text: "No",
            btnClass: 'btn-red',
            action: function () {

            }
        },
    }
});
}



});

