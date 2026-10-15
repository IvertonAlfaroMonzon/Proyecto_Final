Pasos importantes para trabajar en nuestro proyecto de algoritmos:

git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"

Estos dos comandos de aqui sirven para que se configure el cmd o powershell de su computadora con git y github para que puedan subir sus archivos y descargarlos, es decir, sirve para vincular su computadora con su cuenta de github. Este paso solo deben hacerlo la primera vez, luego ya no sera necesario.

Luego deberan crear una carpeta en alguna parte de su computadora, es IMPORTANTE que esa carpeta sea creada fuera de todas las rutas que contenga "ONEDRIVE" porque sera mas dificil de trabajar asi.
En la ventana del cmd escribiran "cd "y aqui iria su ruta de donde hayan creado la carpeta, sin las comillas"

git clone https://github.com/IvertonAlfaroMonzon/Proyecto_Final.git
cd "nombre de su carpeta"

Este codigo sirve para que ustedes clonen el repositorio y todos los archivos que se hayan subido ahi para que los puedan modificar en su computadora.

Git status

Este comando sirve para verificar en donde se encuentran, es decir, si estan en la carpeta correcta y en su rama correspondiente.

git checkout main
git pull origin main

Estos comandos sirven para que descarguen los ultimos cambios que se hayan hecho en el archivo main, es decir, en el archivo principal de nuestro repositorio.

git checkout -b "tuNombre-tarea"

Este comando sirve para crear la rama donde van a trabajar, es importante que creen la rama con un nombre caracteristico de que es lo que van a trabajar, por ejemplo "Iverton-Grafico-Principal" para poder identificar mas facilmente la rama de cada uno, en la rama que ustedes creen es donde van a trabajar cada quien su propio codigo o archivo.

git add

Este comando sirve para añadir lo que tengan creado o modificado, en el caso de que quieran subir todo lo que hayan modificado, el codigo seria "git add ."

git commit -m "descripcion de que es lo que se esta subiendo o modificando"

Este comando sirve para subir los cambios que se realizaron con el anterior codigo de "git add .", porque el comando anterior solo sirve para enlistar los archivos que se subiran, y con este de aqui se suben a la pagina los archivos seleccionados

git push origin tuNombre-tarea

Este comando de aqui es el final para subir los archivos, los dos anteriores sirven para seleccionar y describir lo que subiremos, con este comando de aqui estamos subiendo los archivos locales que modificamos a nuestro repositorio en github. Reemplazen "tunombre-tarea" por el nombre de la rama en donde estan trabajando.

Finalmente repetir estos comandos:
git checkout main
git pull origin main




Los comandos que van a utilizar siempre son:
git checkout main
git pull origin main
git status
git add .
git commit -m
git push origin


Cualquier situacion que suceda, avisar al coordinador del grupo principal (iverton) para poder subir correctamente los archivos o trabajar bien.

Salu2