# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:29:13 2021

@author: Usuario
"""
import pandas as pd
import psycopg2
from ConsultaSFW import ConsultaSFW
from ConsultaSF import ConsultaSF
from ConsultaTotal import ConsultaTotal
import re
import requests
import xml.etree.ElementTree as ET
import html


class ControladorBD:  # TODO: hay que cambiar el nombre a la clase xD
    """
    Clase encargada de la gestión de tablas en una BD en POSTGRESQL.
    Una vez se crea una instancia de esta clase, cuando se vaya a dejar de usar, es necesario emplear el
    método cerrarBD().
    """

    diccionarioConversionLocalidad = [
        'Abanilla', 'Abarán', 'Águilas', 'Albudeite', 'Alcantarilla', 'Aledo', 'Alguazas', 'Alhama de Murcia',
        'Archena', 'Beniel', 'Blanca', 'Bullas', 'Calasparra', 'Campos del Río', 'Caravaca de la Cruz',
        'Cartagena', 'Cehegín', 'Ceutí', 'Cieza', 'Fortuna', 'Fuente Álamo', 'Jumilla', 'La Unión', 
        'Las Torres de Cotillas', 'Librilla', 'Lorca', 'Lorquí', 'Los Alcázares', 'Mazarrón', 'Molina de Segura',
        'Moratalla', 'Mula', 'Murcia', 'Ojós', 'Pliego', 'Puerto Lumbreras', 'Ricote', 'San Javier',
        'San Pedro del Pinatar', 'Santomera', 'Torre Pacheco', 'Totana', 'Ulea', 'Vilanueva del Rio Segura', 'Yecla'
    ]
    
    
    
    def __init__(self, host, database, user, password):
        """
        Establece conexión con el servidor.
        
        PARAMETROS
        ----------
        host : string
            Nombre del host donde se encuentra la base de datos.
        database : string
            Nombre de la base de datos.
        user : string
            Nombre del usuario que accede a la base de datos.
        password : string
            Contraseña que da acceso a la base de datos.

        RETURN
        -------
        None.

        """
        # Atributos privados: conexion y cur
        self.conexion = psycopg2.connect(host = host, database= database, 
                                    user = user, password= password)

        self.cur = self.conexion.cursor()
     
    
    
    
    def cerrarBD(self):
        """
        Cierra la conexión con el servidor de la base de datos.

        RETURN
        -------
        None.

        """
        # Se cierran la conexión y el cursor 
        self.cur.close()
        self.conexion.close()
        
        
    def deleteTabla(self, nombreTabla):
        sql= "DROP table IF EXISTS \"" + nombreTabla + "\""
        self.cur.execute(sql)    # Se realiza la creación de la tabla
        self.conexion.commit() 
        


    def convertCSVtoBD(self, nombreTabla, fileCSV):
        """
        Convierte un fichero .csv a una nueva tabla de la base de datos.
        
        PRECONDICIONES
        ----------
        -La primera columna del csv será el campo por que se identificarán los elementos de la tabla (NOT NULL).
        
        PARÁMETROS
        ----------
        nombreTabla: string
            Nombre de la tabla que se creará en la BD.
        fileCSV: string
            Dirección del fichero .csv de la información de la que se quiere crear una tabla en la BD.
            Se recomienda que siga el siguiente formato: r"direccion".
        
        POSTCONDICIONES
        ----------
        En caso de que no existiese ya esa información en la BD, crea una tabla llamada nombreTabla en la base de datos.
        
        RETURNS
        -------
        None.
        """
        # Se ha decidido que cada función haga su propia conexión, de esta forma se cierra la conexión
        # cuando acaba la acción. La cuestión es que si se realizan muchas pequeñas acciones, se
        # establecerán muchas conexiones para realizar una acciñon pequeña (no es el caso de esta función).
        
        
        # csv: dataframe del que se va a obtener toda la información
        csv = pd.read_csv(fileCSV, delimiter = ';', encoding = 'latin-1')
        
        ###### CREACIÓN DE LA TABLA VACÍA
        # columnas: lista de todos los nombres de columnas
        columnas = csv.columns
        nColumnas = columnas.size
    
        nFilas = int(csv.size / nColumnas)
        
        print("nFilas =  ", nFilas)
        print("nColumnas = ", nColumnas)
         
        # sql contiene el texto con el que se creará la tabla en caso de que no exista en la BD
        sql = "CREATE TABLE IF NOT EXISTS " + nombreTabla
        sql+= "\n\t("
        sql+="\n\t\tID TEXT PRIMARY KEY NOT NULL" # primary key (pk)
        for i in range(1, nColumnas, 1):
            nombreColumna = columnas[i]
            if _isNumero(str(csv.at[0, columnas[i]])):  # Es un número
                sql += ",\n\t\t\"" + nombreColumna + "\" NUMERIC NULL"
            else:                                       #No es un número, por lo que se tratará como texto
                 sql += ",\n\t\t\"" + nombreColumna + "\" TEXT NULL"
            
        sql+= "\n\t)"
        
        self.cur.execute(sql)    # Se realiza la creación de la tabla
        self.conexion.commit()   
            
        
        ###### SE AÑADEN LOS VALORES DEL CSV
        
        # Nota: para que se añada cualquier string de forma literal, se encierra entre $$string$$
        for i in range(0, nFilas, 1):
            sql = "INSERT INTO " + nombreTabla + " VALUES ($$"
            casilla = str(csv.at[i, columnas[0]])
            if self._isNumero(casilla):
                casilla = casilla.replace(",", ".")
            sql += casilla
            for j in range(1, nColumnas, 1):
                casilla = str(csv.at[i, columnas[j]])
                if _isNumero(casilla):
                    casilla = casilla.replace(",", ".")
                sql += "$$, $$" + casilla 
                
            sql += "$$);"
            self.cur.execute(sql)
          
        self.conexion.commit()           
    
        
    def newConvertHTMLtoBD(self, nombreTabla, tipo, localidad):
        # Se obtiene el código de la  localidad a partir del diccionario
        codigoLocalidad = str(ControladorBD.diccionarioConversionLocalidad.index(localidad) + 30001)

        # Se crea la dirección URL de donde se van a obtener los datos
        query_concat = 'http://www.murciaturistica.es/es/rss_brr?tipo=' + tipo + '&localidad=' + codigoLocalidad + '&password=lfbK2RCc41'
        # Ejemplo URL: http://www.murciaturistica.es/es/rss_brr?tipo=restaurantes&localidad=30016password=lfbK2RCc41
        
        respuesta = requests.get(query_concat)

        xml_filename = nombreTabla + '.xml'
        
        # Genera un XML con toda la información obtenida a partir de la url.
        with open(xml_filename,'w') as f:
            f.write(respuesta.text)
        
        tree = ET.parse(xml_filename)
        root = tree.getroot()    
    
        arrayTipos = _getTiposFromXML(xml_filename)   # ESTO ES MUY ARRIESGADO: ASUME QUE EL XML ES PERFECTAMENTE ESTRUCTURADO
        if arrayTipos == None:
            return False
       
        
        setColumnas = []  # "Conjunto" de columnas: lista ordenada que se eliminarán repetidos después
        nItem = -1
        
        for item in root.iter('item'):  # Se recorren los items
            nItem = nItem + 1
            nColumnasItem = len(item)   # Nº de columnas de ese item concreto, por si acaso difieren
            
            insertColumnas = ""   # Campos de columnas para la sentencia SQL INSERT
            insertValues = ""     # Campos de valores para la sentencia SQL INSERT
            sqlINSERT = "INSERT INTO \"" + nombreTabla + "\"\n\t("
            
            # Si es el primer elemento, hay que hacer tratamiento especial para generar la consulta de creación de tabla
            if nItem == 0: 
                
                for i in range(0, nColumnasItem, 1):    # Se recorren las columnas
                    columna = item[i].tag
                    
                    # Si no está la columna, se inserta en la creación de la consulta. Si está, se ignora.
                    if columna not in setColumnas:      
                        setColumnas.append(item[i].tag) 
                        
                        dato = _limpiarFormatoXML(str(item[i].text).strip())         # Valor de la columna
                        
                        if i == 0: # La primera columna recibe tratamiento especial
                            sqlCreacion = "CREATE TABLE IF NOT EXISTS \"" + nombreTabla + "\"\n\t(" 
                            insertColumnas += "\"" + columna + "\""
                            
                            if dato == None or dato == "None":
                                insertValues += "NULL"
                            else:
                                insertValues += "$$" + dato + "$$"
                                                    
                            if arrayTipos[0] == 'n':  # Es un número
                               sqlCreacion += "\n\t\t\"" + columna + "\" NUMERIC PRIMARY KEY NOT NULL"
                            else:                     # Es un texto
                               sqlCreacion += "\n\t\t\"" + columna + "\" TEXT PRIMARY KEY NOT NULL" 
                               
                        else:   # No es la primera columna
                            insertColumnas += ", \"" + columna + "\""
                            
                            if dato == None or dato == "None":
                                insertValues += ", NULL"
                            else:
                                insertValues += ", $$" + dato + "$$"
                                
                            if arrayTipos[i] == 'n':  # Es un número
                                sqlCreacion += ",\n\t\t\"" + columna + "\" NUMERIC NULL"
                            else:                                       #No es un número, por lo que se tratará como texto
                                sqlCreacion += ",\n\t\t\"" + columna + "\" TEXT NULL"       
                sqlCreacion+= "\n\t)"
                
                print("\n\n########CREACION TABLA")    
                print(sqlCreacion)
                    
                # Se ejecuta la sentencia SQL para la creación de la tabla y se confirma
                self.cur.execute(sqlCreacion)
                self.conexion.commit()
                            
            
            else:  # No es el primer elemento
                setColumnaItem = []
                for i in range(0, nColumnasItem, 1):    # Se recorren las columnas
                    columna = item[i].tag
                    dato = _limpiarFormatoXML(str(item[i].text).strip())         # Valor de la columna
                    
                    # Si no está la columna, hay que añadirla a la tabla.
                    if columna not in setColumnas:      
                        # Se crea sentencia SQL para añadir la nueva columna
                        sqlNewRow = "ALTER TABLE " + nombreTabla + " ADD COLUMN \"" + columna + "\""
                        if _isNumero(dato):
                            sqlNewRow += "NUMERIC NULL;"
                        else: 
                            sqlNewRow += "TEXT NULL;"
                        print("\n\n########## ADD COLUMN ", columna)
                        self.cur.execute(sqlNewRow)
                        self.conexion.commit()
                        
                    else:   # Hay que añadir la columna a la tabla
                        setColumnas.append(item[i].tag)                         
                   
                    # Si no está la columna, se inserta en la creación de la consulta. Si está, se ignora porque está duplicado
                    if columna not in setColumnaItem:
                        setColumnaItem.append(columna)
                        
                        if i == 0: # La primera columna recibe tratamiento especial
                            insertColumnas += "\"" + columna + "\""
                            if dato == None or dato == "None":
                                insertValues += "NULL"
                            else:
                                insertValues += "$$" + dato + "$$"
                        else:     # No es la primera columna
                             insertColumnas += ", \"" + columna + "\""
                             if dato == None or dato == "None":
                                insertValues += ", NULL"
                             else:
                                insertValues += ", $$" + dato + "$$"
                          
            
            sqlINSERT += insertColumnas + ") VALUES (" + insertValues + ");"
            print("\n\n###### INSERT")
            print(sqlINSERT)
            self.cur.execute(sqlINSERT)
            self.conexion.commit()
            
        return True                  
    

                    
                
            
            
        
    
    
    def convertHTMLtoBD(self, nombreTabla, tipo, localidad): #TODO añadir conversión de localidad-codigo para que no haya necesidad de saberselos
        """
        A partir del tipo de datos que se quiere obtener información y de la localidad, genera una tabla en la BD.

        PARÁMETROS
        ----------
        nombreTabla : string
            Nombre de la tabla que se creará en la BD.
        tipo : string
            Información que se quiere obtener.
        localidad : string
            Nombre de la localidad.

        RETURN
        -------
        Devuelve True si se ha añadido con éxito la información. False en caso contrario.
        
        POSTCONDICIÓN
        -------------
        En caso de que no existiese ya esa información en la BD, crea una tabla llamada nombreTabla en la base de datos.
        """
        
        # Se obtiene el código de la  localidad a partir del diccionario
        codigoLocalidad = str(ControladorBD.diccionarioConversionLocalidad.index(localidad) + 30001)

        # Se crea la dirección URL de donde se van a obtener los datos
        query_concat = 'http://www.murciaturistica.es/es/rss_brr?tipo=' + tipo + '&localidad=' + codigoLocalidad + '&password=lfbK2RCc41'
        # Ejemplo URL: http://www.murciaturistica.es/es/rss_brr?tipo=restaurantes&localidad=30016password=lfbK2RCc41
        
        respuesta = requests.get(query_concat)

        xml_filename = nombreTabla + '.xml'
        
        # Genera un XML con toda la información obtenida a partir de la url.
        with open(xml_filename,'w') as f:
            f.write(respuesta.text)
        
        tree = ET.parse(xml_filename)
        root = tree.getroot()
    

        #TODO AEROPUERTOS DA FALLO PORQUE NO TIENE CAMPO ITEM SINO CHANNEL
        #NOTA: NO HAY CAMPO ITEM, YA QUE EN CARTAGENA NO HAY AEROPUERTOS
        #HAY QUE HACER COMPROBACIÓN SEMEJANTE A iter.hasNext().
        #Es decir, hay que ver si hay item antes de hacer next()     
        # Lista que indica si es un  texto o número. Si la posición tiene un 1 es texto. 0 si es numero.
 
        arrayTipos = _getTiposFromXML(xml_filename)
        if arrayTipos == None:
            return False
        
        
        print("###################CREACION DE LA TABLA")
        
        # PROCESO DE OBTENCIÓN DE COLUMNAS DE UNA TABLA

        iterador = root.iter('item')

        item = iterador.__next__() # Se obtiene el primer elemento para obtener las columnas de la tabla

            
        print(item)
        nColumnas = len(item)
        print("Número de campos : ", nColumnas)

        
        
        sql = "CREATE TABLE IF NOT EXISTS \"" + nombreTabla
        sql+= "\"\n\t("
        
        nombreColumna = item[0].tag
        
        if arrayTipos[0] == 'n':  # Es un número
            sql += "\n\t\t\"" + nombreColumna + "\" NUMERIC PRIMARY KEY NOT NULL"
        else:                                       #No es un número, por lo que se tratará como texto
            sql += "\n\t\t\"" + nombreColumna + "\" TEXT PRIMARY KEY NOT NULL"
        
        for i in range(1, len(item), 1):  # Se obtienen todos los campos de la tabla
            print(i, "= ", item[i].tag)
            print(item[i].text)
        
            nombreColumna = item[i].tag
                
            if arrayTipos[i] == 'n':  # Es un número
                sql += ",\n\t\t\"" + nombreColumna + "\" NUMERIC NULL"
            else:                                       #No es un número, por lo que se tratará como texto
                sql += ",\n\t\t\"" + nombreColumna + "\" TEXT NULL"
                
        sql+= "\n\t)"
                
        print(sql)        
        self.cur.execute(sql)
        self.conexion.commit()
        
        
        
        ## PROCESO DE LLENADO DE LA TABLA
        print("\n\n############ SE COMIENZA A RELLENAR LA TABLA ##############")
        for item in root.iter('item'):
            sql = "INSERT INTO \"" + nombreTabla + "\" VALUES ("
            # Tratamiento del primer elemento
            casilla = str(item[0].text)
            print("casilla: ", casilla)
            print("Tipo: ", arrayTipos[0])
            if casilla == None or casilla == "None":
                    sql += "NULL"
            else:
                if arrayTipos[0] == 't':   # El primer elemento es texto
                    print(casilla, " es un texto")
                    casilla = _limpiarFormatoXML(casilla)
                    sql += "$$" + casilla + "$$"
                else:                      # El primer elemento es un número
                    sql += casilla
                
            for i in range(1, nColumnas, 1):
                casilla = str(item[i].text)
                print("casilla i: ", casilla)
                print("Tipo i: ", arrayTipos[i])
                if casilla == None or casilla == "None":
                    sql += ", NULL"
                else:
                    if arrayTipos[i] == 't':   # El primer elemento es texto
                        print(casilla, " es un texto")
                        casilla = _limpiarFormatoXML(casilla.strip())
                        sql += ", $$" + casilla + "$$"
                    else:                      # El primer elemento es un número
                        sql += ", " + casilla
                        
            sql += ");"
            print("INSERCION EN LA TABLA: ")
            print(sql)
            self.cur.execute(sql)
            self.conexion.commit()
            print(sql)
            
        
    
    def consultar(self, tabla, selectLista="None", condicion="", nombreFicheroSalida="", tipoFicheroSalida=""):
        """
        Realiza una consulta en la base de datos.
        Las columnas si tienen un número serán tipo NUMERIC. En caso contrario, TEXT.
        Si no se indican nombre de fichero de salida o su tipo, no se generará fichero de salida.  
        Si el tipo de fichero de salida no coincide con ninguno válido, no se generará fichero de salida.
        Si no se indica la selectLista, la consulta se hará a todas las columnas.
        
        PARAMETROS
        ----------
        tabla: string
            Nombre de la tabla que se consulta.
        selectList (opcional) : lista string
            Nombre de las columnas de salida en la consulta.
        condicion (condicional): string
            Condiciones que debe cumplir la consulta.
        nombreFicheroSalida (opcional): string    
            Nombre del fichero de salida.
        tipoFicheroSalida (opcional): string
            Tipo del fichero de salida.

        RETURNS
        -------
        None.
        
        POSTCONDICIONES
        ---------------
        Si el nombre y tipo de fichero de salida son válidos, se generará un fichero de salida con el 
        formato indicado. En caso contrario, saldrá en formato lista de tuplas por pantalla.
        

        """
        if selectLista == "":  # Consulta de tipo *, hay que obtener los nombres de las columnas de la tabla
            print("dentro")
            consulta = ConsultaTotal(nombreFicheroSalida, tipoFicheroSalida)
            
            # Hay que obtener estos nombres a partir de la metainformación de la BD
            sql =  "SELECT COLUMN_NAME\n"
            sql += "FROM INFORMATION_SCHEMA.COLUMNS\n" 
            sql += "WHERE table_name = '" + tabla + "'\n"
            sql += "ORDER BY ordinal_position"
            self.cur.execute(sql)
            print(sql)
            consultaNombresColumnas = self.cur.fetchall()
            lista = []
            for i in range(0, len(consultaNombresColumnas), 1):
                print("i= ", consultaNombresColumnas[i][0])
                lista.append(consultaNombresColumnas[i][0])
            
            consulta.realizarConsulta(tabla, lista, condicion, self.cur)
            
        else:
            if condicion =="":
                consulta = ConsultaSF(nombreFicheroSalida, tipoFicheroSalida)
            else:
                consulta = ConsultaSFW(nombreFicheroSalida, tipoFicheroSalida)
            consulta.realizarConsulta(tabla, selectLista, condicion, self.cur)
        

#################### SECCIÓN DE FUNCIONES PRIVADAS    
def _isNumero(s):
    """
    Comprueba si s es un número o no.

    PARAMETROS
    ----------
    s : string
    Cadena de texto a comprobar.

    RETURNS
    -------
    boolean: si s es un numero devuelve True, False en caso contrario.
    """ 
    # Expresión regular que determina un entero o double con o sin signo
    pattern = '((\+|-)?[0-9]+((\.|,)[0-9]+)?)'
    comprobacion = re.fullmatch(pattern, s)
    if comprobacion: 
        return True
    else:    
        return False  
    
        
def _limpiarFormatoXML(s):
    """
    Limpia el formato proporcionado como entrada borrando ciertos elementos como '\n' o formatos propios de XML.

    PARÁMETROS
    ----------
    s : string
        Cadena de texto

    RETURN
    -------
    Cadena de texto formateada.

    """
    if s == "" or s == None or s=="None" :
        return s
    
    
    s = s.replace('\n','') if s is not None else s
    s = s.replace('<br />', "") if s is not None else s
    s = s.replace('<br>', "") if s is not None else s
    s = s.replace('<p>', "") if s is not None else s
    s = s.replace('</p>', "") if s is not None else s
    s = s.replace('<strong>', "") if s is not None else s
    s = s.replace('</strong>', "") if s is not None else s
    s = s.replace('</span>', "") if s is not None else s
    s = s.replace('\xa0', "") if s is not None else s
    s = s.replace('<span style="font-size:13px">', "") if s is not None else s
    s = s.replace('<span style="font-size:14px">', "") if s is not None else s
    
    # Eliminar expresiones del tipo <a...> ... </a>:
    # MIENTRAS sigaHabiendoExpresionesDeEsteTipo HACER
    #   BORRAR EXPRESION
    pattern = '<a.*?<\/a>'              # Expresión regular que define este formato
    # pattern = r'<a.*?<\/a> ?(\(\d+ ?.+?\))?'  # EXPRESIÓN BUENA, PERO NO FUNCIONA
                                                # Al final de esa expresión puede haber "(4 Mb)" que se queda
    matches = re.findall(pattern, s)    # Se encuentran todas las coincidencias con este formato
    for i in range(0, len(matches), 1):
        s = s.replace(matches[i], '')   # Se borran todas y cada una de ellas
        
    return s
    


def _getTiposFromXML(xml_filename):
    """
    Obtiene los tipos de cada una de las 

    PARÁMETROS
    ----------
    xml_filename : TYPE
        DESCRIPTION.

    RETURN
    -------
    List of char
        Tipos de char:
            -'t': texto
            -'n': número
        Valor por defecto: 't'
            
    None en caso de que no hayan filas "item"
    """
    
    valorDefecto = 't'  # Cuando no hay ningún valor en toda la columna

    
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    iterador = root.iter('item')
    
    # CÓDIGO PARA SABER SI HAY ELEMENTOS
    try:
        item = iterador.__next__() # Se obtiene el primer elemento para obtener las columnas de la tabla
        
    except StopIteration:
        print("No hay items.")
        return None
    
    # HAY ELEMENTOS, POR TANTO, SE PROCEDE A OBTENER LOS TIPOS
    nCampos = len(item)
    
    # Se inicializa la variable de salida
    tipos=[]
    
    for i in range(0, nCampos, 1):
        tipos.append('')
    
    for i in range(0, nCampos, 1):
        iterador = root.iter('item')
        item = iterador.__next__() 
        encontrado = False
        casilla = _limpiarFormatoXML(item[i].text)    
        
        while not encontrado:
            print(casilla)
            if casilla != None:  # Es algo, por lo que puede ser un texto o un número, se parsea para saberlo
                if _isNumero(casilla):   # Es un número
                    tipos[i] = 'n'  
                    # Hay que comprobar si después va a haber un campo de esa misma columna como texto
                    try:
                        item = iterador.__next__() # Se pasa al siguiente item
                        casilla = _limpiarFormatoXML(item[i].text)   
                    except StopIteration: 
                        # Se ha llegado al final de los items, por lo que la columna entera está formada por números                        
                        encontrado = True
                else:                    # Es texto
                    tipos[i] = 't'
                    encontrado = True
                
            else:    # Se ha encontrado None: se pasa al siguiente item
                try:
                    item = iterador.__next__() # Se obtiene el primer elemento para obtener las columnas de la tabla
                except StopIteration: 
                    # Se ha llegado al final de los items, por lo que la columna entera está vacía
                    tipos[i] = valorDefecto
                    
                    encontrado = True
     
        
    return tipos















