pay = [{opccion:"usuarios"},{opccion:"vacantes"},{opccion:"candidatos"},{opccion:"pruebaspscometricas"}];// opciones de las colecciones de payempleos
basesirec = [{opccion:"usuarios"},{opccion:"clientes"},{opccion:"reportes"}]; // opciones de coleciones de base-sirec
sistema_info = [{opccion:"usuarios"}];// opciones de las colecciones de sistemas de informacion.

selectSistema = document.getElementById('sistema'); // btencion del select sistema
selectColeccion = document.getElementById('respaldo');// obtencion del select de respaldo esto para seleccionar la coleccion que se desea hacer respaldo
radioUno = document.getElementById('uno'); // radio uno
radioTodo = document.getElementById('todo');// radio todo
btnCrear = document.getElementById/('crear');// boton de crear
formulario = document.getElementById('formulario');// formulario
  
radioUno.addEventListener('change',()=>{ //evento de cambio checkbox  
    if (radioUno.checked){
        radioTodo.checked = false; // cambia el check box de todo a falso 
        selectColeccion.hidden = false;// cambia el oculto(hidden) de select de 
        selectSistema.hidden = false;// cambia el oculto(hidden) de select de coleccion
        formulario.action = "/datos_coleccion" // cambio de action al formulario 
    }
})

radioTodo.addEventListener('change',()=>{ // evento de cambio de checkbox 
    if (radioTodo.checked){
        radioUno.checked = false;
        selectColeccion.hidden = true;
        selectSistema.hidden = true;
        formulario.action = "/datos_completos"
    }
})

selectSistema.addEventListener('change',()=>{ // evento para cambiar las opciones de selectColeccion
    selectColeccion.innerHTML = "";
    switch(selectSistema.value){
        case 'payempleos':
            pay.forEach(opcion => {   // lee los datos de objetos de las colecciones de pay para establecerlas en en el select
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break;
        case 'base-sirec':
            basesirec.forEach(opcion => {  // lee los datos de objetos de las colecciones de base sirec para establecerlas en en el select
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break;
        case 'sistemas-de-informacion':
            sistema_info.forEach(opcion => { // lee los datos de objetos de las colecciones de sistemas de informacion para establecerlas en en el select
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break    
    }
})

