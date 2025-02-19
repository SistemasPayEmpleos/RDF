pay = [{opccion:"usuarios"},{opccion:"vacantes"},{opccion:"candidatos"},{opccion:"pruebaspscometricas"}];
basesirec = [{opccion:"usuarios"},{opccion:"clientes"},{opccion:"reportes"}];
sistema_info = [];

selectSistema = document.getElementById('sistema');
selectColeccion = document.getElementById('respaldo');

selectSistema.addEventListener('change',()=>{
    selectColeccion.innerHTML = "";
    switch(selectSistema.value){
        case 'payempleos':
            pay.forEach(opcion => {
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break;
        case 'base-sirec':
            basesirec.forEach(opcion => {
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break;
        case 'sistemas-de-informacion':
            sistema_info.forEach(opcion => {
                const option = document.createElement('option');
                option.value = opcion.opccion;
                option.textContent = opcion.opccion;
                selectColeccion.appendChild(option);
            });
            break    
    }
})