from fpdf import FPDF  # libreria para tratar el pdf
import pandas as pd  # extraccion y transformaciond e datos ETL
import sys  # Ambas librerias sys y signal, controlaran salida
import signal
import re
# Tanto seaborn y matplotlib son para creacion de graficas lanzadas con python
import seaborn as sns
# empleada para sacar n menores o n mayores de una lista
import matplotlib.pyplot as plt
# importamos las librerias necesarias


class pdf(FPDF):
    # Esta clase esta basada en un video tutorial de yt que encontre
    # no obstante está amoldada a mis necesidades
    def portada(self):  # funcion empelada para crear la primera pagina de mi pdf será portada
        self.add_page()
        self.set_font('Times', 'B', 35)
        self.cell(w=210.0, h=20.0, align='C',
                  txt="MAVEN PIZZAS 2016", border=False, ln=True)
        self.cell(w=190.0, h=19.0, align='C',
                  txt="REPORTE EJECUTIVO", border=False, ln=True)
        self.image('logo.png', 32, 100, 150)

    # funcion empleada para lanzamiento graficas pizzas y precios
    def pizzas_semanales_precios(self):
        self.add_page()  # Abrimos una nueva pagina
        self.set_font("Times", "BU", 25)
        self.set_xy(0, 12)
        self.cell(w=220.0, h=18.0, align='C',
                  txt="Precios y Top Pizzas", border=False, ln=True)
        self.image("barplot_Top_5_pizzas.png",  30, 30, 150, 90)

    def analisis_total_ingredientes(self):
        self.add_page()  # Nueva pagina de mi pdf diseñado para el estudio de los ingredientes
        self.set_font("Times", "BU", 25)
        self.cell(w=220.0, h=18.0, align='C',
                  txt="ANALISIS SEMANAL INGREDIENTES", border=False, ln=True)
        self.set_xy(0, 12)
        self.image("barplot_ingredientes.png", 30, 30, 150, 90)

    def analisis_top_ingredientes(self):
        self.add_page()  # Nueva pagina de mi pdf diseñado para el estudio de los ingredientes
        self.set_font("Times", "BU", 25)
        self.cell(w=220.0, h=18.0, align='C',
                  txt="ANALISIS  SEMANAL INGREDIENTES", border=False, ln=True)
        self.set_xy(0, 12)
        self.image("barplot_Top_10_ingredientes.png", 30, 30, 150, 90)


def handler_signal(signal, frame):  # funcion de salida controlada
    print("\n\n Interrupcion del programa, saliendo del prograam de manera controlada y ordenada")
    sys.exit(1)


# Ctrl + C, en caso de introducirlo por teclado saldremos del programa
signal.signal(signal.SIGINT, handler_signal)


def extract_and_transform():  # extraccion y transformacion dataset de order details
    pedidos_detallados = pd.read_csv(
        "order_details.csv", sep=";", encoding="latin1")
    pedidos_detallados = pedidos_detallados.dropna()
    pedidos_detallados.reset_index(inplace=True)
    lista = []
    lista_mala = []
    for pizza in range(0, len(pedidos_detallados['pizza_id'])):
        lista_mala.append(pizza)
        a = re.sub('@', 'a', pedidos_detallados['pizza_id'][pizza])
        b = re.sub('0', 'o', a)
        c = re.sub('3', 'e', b)
        e = re.sub(' ', '_', c)
        f = re.sub('-', '_', e)
        lista.append(f)
    pedidos_detallados["pizza_id"] = lista
    return pedidos_detallados


def extract():
    # En nuestro caso no será necesario extraer la informacion del csv de las orders
    # puesto que nos basaremos en calcular todos las pizzas pedidas en un año y despues
    # dividiremos entre el numero de semanas
    ingredientes = pd.read_csv("pizza_types.csv", sep=",", encoding="LATIN-1")
    pizzas = pd.read_csv("pizzas.csv", sep=",", encoding="UTF-8")
    pedidos_detallados = extract_and_transform()
    # En nuestro caso no será necesario extraer la informacion del csv de las orders
    # puesto que nos basaremos en calcular todos las pizzas pedidas en un año y despues
    # dividiremos entre el numero de semanas
    return ingredientes, pizzas, pedidos_detallados


# funcion realizada para limpiar la columna de cantidad d eorders_details
def cambias_one_1(pedidos_detallados):
    lista = []
    lista_mala = []
    # empelamos regex a cada una de las cantidades, hasta tenee valores enteros 1 o 2
    for cantidad in range(0, len(pedidos_detallados["quantity"])):
        lista_mala.append(cantidad)
        a = re.sub('one', '1', pedidos_detallados['quantity'][cantidad])
        b = re.sub('0ne', '1', a)
        c = re.sub('One', '1', b)
        e = re.sub('two', "2", c)
        f = re.sub("-1", "1", e)
        lista.append(int(f))
    # despues establecemos  los cambios en columna correspondiente
    pedidos_detallados["quantity"] = lista
    return pedidos_detallados


def diccionario_ingredientes(ingredientes):
    diccionario_ingredientes = {}  # Creamos un diccionario vacio
    lista_uncia = []  # Tenemos una lista vacia
    # nos pasamos lo singredientes a una lista
    lista_ingredientes = ingredientes["ingredients"].tolist()
    for i in range(len(lista_ingredientes)):  # Recorremos dicha lista
        # Separamos los ingredientes asociados a cada una de las pizzas y las convertimos en llave de mi diccionario
        separaciones = lista_ingredientes[i].split(", ")
        for j in range(len(separaciones)):
            if separaciones[j] not in lista_uncia:
                a = separaciones[j]
                lista_uncia.append(a)
    for i in lista_uncia:
        # Inicializamos todo ingrediente(llave de mi diccioanrio) a valor 0
        diccionario_ingredientes[i] = 0
    # Devolvemos el diccioanrio que tiene por clave todo los ingredienets y como valores todo 0
    return diccionario_ingredientes


def ing_pizza(ingredientes):  # Funcion encargada de definir que ingredienets tiene cada pizza
    diccionario_ingredientes_por_pizza = {}  # Creamos un diccionario nuevo
    # extraemos nombre generico sin tamaño
    tipo_pizza_generico = ingredientes["pizza_type_id"].to_list()
    #  Sacamos todos los ingredienets asociados a cada pizza
    lista_ingredientes = ingredientes["ingredients"].tolist()
    lista_nueva = []  # inicializamos lista vacia
    for ing_p in lista_ingredientes:
        lista_nueva.append(ing_p.split(", "))

    for i in range(len(tipo_pizza_generico)):
        diccionario_ingredientes_por_pizza[tipo_pizza_generico[i]
                                           ] = lista_nueva[i]
    return diccionario_ingredientes_por_pizza


def ponderacion_semanal(ingredientes, pedidos_detallados):
    pizzas_numero_anual = {}
    tipos_pizza = pedidos_detallados["pizza_id"].unique().tolist()
    for pizza in tipos_pizza:
        pizzas_numero_anual[pizza] = pedidos_detallados[pedidos_detallados["pizza_id"]
                                                        == pizza]["quantity"].sum()
    # ahora tendria en el diccionario el numeor de pizzas anuales
    # paar saber las semanas dividire entre 51, a pesar de que un año tenga 52 semanas con el fin de prevenir una semana de mayor media
    pizzas_numero_semanal = {}
    for pizza in tipos_pizza:
        # el mas 1 lo sumaremos para tener en cuenta aquellas pizzas que no llegan siquiera a 1 por semana
        pizzas_numero_semanal[pizza] = pizzas_numero_anual[pizza] // 51 + 1
    # los tipos de pizza seran nuestras pizzas sin tener en cuenta tamaños
    tipo_pizza = ingredientes["pizza_type_id"].tolist()
    # Los valores de nuestro diccionario serán los ingredientes
    tamaños = ["m", "s", "l", "xl", "xxl"]
    diccionario_pizzas = {}
    nombres_pizzas_genericos = list(ingredientes["pizza_type_id"])
    for nombre in nombres_pizzas_genericos:
        diccionario_pizzas[nombre] = 0

    for pizza in tipos_pizza:  # Bucle realizado para eliminar el tamaño de pizzas para facilitarnos lectura posterior
        # Realizado una vez se ha tenido en cuenta la ponderaion por tamaños
        a = str(pizza)
        if "_s" in a:
            numero_pizzas = pizzas_numero_semanal[pizza]
            nm = a[:-2]
            diccionario_pizzas[nm] += numero_pizzas
        if "_m" in a:
            numero_pizzas = pizzas_numero_semanal[pizza] * 2
            nm = a[:-2]
            diccionario_pizzas[nm] += numero_pizzas

        if "_l" in a:
            numero_pizzas = pizzas_numero_semanal[pizza] * 3
            nm = a[:-2]
            diccionario_pizzas[nm] += numero_pizzas

        if "_xl" in a:
            numero_pizzas = pizzas_numero_semanal[pizza] * 4
            nm = a[:-3]
            diccionario_pizzas[nm] += numero_pizzas

        if "_xxl" in a:
            numero_pizzas = pizzas_numero_semanal[pizza] * 5
            nm = a[:-4]
            diccionario_pizzas[nm] += numero_pizzas
    return diccionario_pizzas


def tabla_ingredientes(df_pizzas_semana, pdf):
    lista_pizza_name = df_pizzas_semana["Pizza"].to_list()
    lista_cantidad = df_pizzas_semana["Quantity"].to_list()
    valores = []
    for i in range(len(lista_pizza_name)):
        valores[i].append(lista_pizza_name[i], lista_cantidad[i])
    for valor in lista_cantidad:

        pdf.cell(w=20, h=9, txt=str(valor[0]), border=1,
                 align='C', fill=0)

        pdf.cell(w=40, h=9, txt=valor[1], border=1,
                 align='C', fill=0)

        pdf.cell(w=70, h=9, txt=valor[2], border=1,
                 align='C', fill=0)

        pdf.multi_cell(w=0, h=9, txt=valor[3], border=1,
                       align='C', fill=0)


def transform(ingredientes, pizzas, pedidos_detallados):
    pedidos_detallados = cambias_one_1(pedidos_detallados)
    # contenido practica 1
    # diccionario inicializado a 0 con el numero de ingredientes de cada tipo
    diccionario_ingredientes_0 = diccionario_ingredientes(ingredientes)
    # diccionario con ingredientes por pizza
    ingredientes_cada_pizza = ing_pizza(ingredientes)
    # diccionario con numero pizzas semanales con ponderacion por tamaño
    pizzas_semana = ponderacion_semanal(ingredientes, pedidos_detallados)
    return pizzas_semana, ingredientes_cada_pizza, diccionario_ingredientes_0


def load(diccionario_ingredientes_0, ingredientes_cada_pizza, pizzas_semana, tipo_pizza_generico):
    for pizza in tipo_pizza_generico:  # por ultimo una vez tenemos los tres diccionarios, el  contadorde los ingredientes,
        # el de piizza con sus respectivos ingredientes y las pizzas semana, sacamos ingredientes semana
        a = pizzas_semana[pizza]
        lista_ing = ingredientes_cada_pizza[pizza]
        for ing in lista_ing:
            diccionario_ingredientes_0[ing] += a
    return diccionario_ingredientes_0


def grafica_ingredientes_semana(df_ing):
    # permite indicar el nº de la figura y las dimensiones (ancho y alto)
    fig = plt.figure(figsize=(10, 10))
    sns.barplot(data=df_ing.sort_values(by='Quantity', ascending=False), x='Quantity', y='Ingredients',
                palette=sns.color_palette('flare', len(df_ing)))
    plt.title("Ingredientes Semanales", fontsize=20)
    plt.xlabel('cantidad')
    plt.ylabel('Ingredientes')
    plt.savefig("barplot_ingredientes.png", bbox_inches='tight')


def top_and_least_10_ing(df_ing):
    sns.set_style('darkgrid')
    # permite indicar el nº de la figura y las dimensiones (ancho y alto)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 5))
    ingredientes = df_ing.sort_values(by='Quantity', ascending=False)
    sns.barplot(data=ingredientes[:10], x='Quantity', y='Ingredients',
                palette=sns.color_palette('Greens', 10), ax=ax1)
    ax1.set_title('Ingredientes_mas_usados', fontsize=15)
    ax1.set_xlabel('Cantidad')
    ax1.set_ylabel("Ingredientes")

    pizzas_sorted_quantity = df_ing.sort_values(by='Quantity', ascending=False)
    sns.barplot(data=pizzas_sorted_quantity[-10:], x='Quantity',
                y='Ingredients', palette=sns.color_palette('Blues', 10), ax=ax2)
    ax2.set_title('Ingredientes_menos_usados', fontsize=15)
    ax2.set_xlabel('Cantidad')
    ax2.set_ylabel("Ingredientes")

    fig.suptitle("Ingredientes Empleados.", fontsize=20)
    fig.tight_layout()
    plt.savefig("barplot_Top_10_ingredientes.png", bbox_inches='tight')


def precios_mas_pedidas_pizzas(pizzas, df_pizzas_semana):
    sns.set_style('darkgrid')
    # permite indicar el nº de la figura y las dimensiones (ancho y alto)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

    pizzas_sorted_price = pizzas.sort_values(by='price', ascending=False)
    sns.barplot(data=pizzas_sorted_price[:5], x='price',
                y='pizza_id', palette=sns.color_palette('Greens', 5), ax=ax1)
    ax1.set_title('Pizzas_mas_caras', fontsize=15)
    ax1.set_ylabel('Prices pizzas')
    ax1.set_xlabel("Pizza ID's")

    pizzas_sorted_quantity = df_pizzas_semana.sort_values(
        by='Quantity', ascending=False)
    sns.barplot(data=pizzas_sorted_quantity[:5], x='Quantity',
                y='Pizza', palette=sns.color_palette('Blues', 5), ax=ax2)
    ax2.set_title('Pizzas_mas_vendidass', fontsize=15)
    ax2.set_ylabel('Top pizzas')
    ax2.set_xlabel("Pizza ID's")

    plt.suptitle("Pizzas, precio y cantidad vendida.", fontsize=20)
    plt.savefig("barplot_Top_5_pizzas.png", bbox_inches='tight')


def creacion_reporte():
    reporte_ejecutivo = executive_report = pdf(
        orientation='P', unit='mm', format='A4')  # creamos un objeto tipo pdf
    reporte_ejecutivo.set_author("Antonio Mora Abos")
    reporte_ejecutivo.portada()  # llamamos a portada
    # llamamos a analisis total ingredientes
    reporte_ejecutivo.analisis_total_ingredientes()
    reporte_ejecutivo.analisis_top_ingredientes()
    # analisisprecio y pizzas mas vendidas
    reporte_ejecutivo.pizzas_semanales_precios()
    reporte_ejecutivo.output("REPORTE_EJECUTIVO.pdf", "F")


if __name__ == "__main__":
    ingredientes, pizzas, pedidos_detallados = extract()
    tipo_pizza_generico = ingredientes["pizza_type_id"].to_list()
    pizzas_semana, ingredientes_cada_pizza, diccionario_ingredientes_0 = transform(
        ingredientes, pizzas, pedidos_detallados)
    diccionario_ingredientes = load(
        diccionario_ingredientes_0, ingredientes_cada_pizza, pizzas_semana, tipo_pizza_generico)
    df_ingredientes = pd.DataFrame([[key, diccionario_ingredientes[key]]
                                    for key in diccionario_ingredientes.keys()], columns=['Ingredients', 'Quantity'])
    df_pizzas_semana = pd.DataFrame([[key, pizzas_semana[key]]
                                     for key in pizzas_semana.keys()], columns=['Pizza', 'Quantity'])
    grafica_ingredientes_semana(df_ingredientes)
    top_and_least_10_ing(df_ingredientes)
    precios_mas_pedidas_pizzas(pizzas, df_pizzas_semana)
    creacion_reporte()
