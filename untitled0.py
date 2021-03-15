# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 17:45:49 2021

@author: Usuario
"""
import xml.etree.ElementTree as ET
import re

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
    print("Número de campos : ", nCampos, "\n\n")
    
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
            if casilla != None:  # Es algo, por lo que puede ser un texto o un número, se parsea para saberlo
                if _isNumero(casilla):   # Es un número
                    tipos[i] = 'n'  
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
                
        print("i= ", tipos[i])
    for i in range(0, nCampos, 1):
        print(i, ": ", tipos[i])
        
    return tipos

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
        print(s, " es un numero")
        return True
    else:    
        print(s, " no es un numero")
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
       
    
