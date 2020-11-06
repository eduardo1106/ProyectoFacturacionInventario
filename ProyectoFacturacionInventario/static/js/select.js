
function select(){
	
	// Calculo del subtotal
var cant=document.getElementById('cant').value;
var prec=document.getElementById('prec').value;  
    
    
    subtotal = cant * prec;
	subtot.value=subtotal;
	
        //Calculo del total
	total = eval(inputtotaltext.value);
	inputtotaltext.value = total + subtotal;
}