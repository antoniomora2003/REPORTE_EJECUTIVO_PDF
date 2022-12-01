# REPORTE_EJECUTIVO_PDF
Repositorio empleado para lanzar un pdf ejecutivo, con la cantidad de ingredientes semanales que deberá comprar el CEO de Maven Pizzas para la siguiente semana. Para el lanzamiento de dicho pdf hemos empleado una serie de librerías, en primer lugar pandas para el tratamiento de los dataframes y su respectiva limpieza, seaborn y matplotlib, para graficar, sys y signal, para la creación de un manejador de señales, que me permita cerrar el programa. 

Lo primero será realizar dicha predicción de ingredientes semanales, para ello primero limpiaremos los dataframes que se nos dan, después crearemos una serie de diccionarios, y jugaremos con ellos y su información con el fin de generar un dataframe final con los ingredientes necesarios para una semana. Después realizamos las graficas necesarias con las librerías de matplotlib y de seaborn. 

La parte más peculiar es el lanzamiento del pdf, para realizarlo hemos acudido a diversos tutoriales de fpdf, y a stackoverflow, con el fin de documentarnos, una vez nos documentamos, hemos creado la clase fpdf, con la ayuda de la librería que tiene ese mismo nombre, y hemos realizado finalmente el pdf.
![image](https://user-images.githubusercontent.com/112613575/205181851-cc4ddde0-f8b2-4a96-b888-4ab1297ec421.png)
