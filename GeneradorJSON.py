# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:53:39 2021

@author: Usuario
"""
from GeneradorSalida import GeneradorSalida
import re

class GeneradorJSON(GeneradorSalida):
    
    def __init__(self):
        GeneradorSalida.__init__(self)
    
    
    def generar(self, resultadoConsulta, listaColumnasConsulta, nombreFicheroSalida):
        """
        Genera fichero .json a partir de la salida de una consulta y de la lista de las columnas a mostrar.

        PARÁMETROS
        ----------
        resultadoConsulta : string
            Salida de la consulta a la base de datos.
        listaColumnasConsulta : lista de string
            Lista de las columnas pedida en la sentencia SELECT.
        nombreFicheroSalida: string
            Nombre del fichero .json que contendrá el resultado de la consulta. No incluir la terminación .json
        
        RETURNS
        -------
        None.
        
        POSTCONDICIONES
        ---------------
        Genera un fichero .json con la salida de la consulta y nombre nombreFicheroSalida.json

        """
        print("EN GENERADOR JSON: ")
        print(listaColumnasConsulta)
        file = open(nombreFicheroSalida + ".json", "w")
                
        nFilasConsulta = len(resultadoConsulta)
        nColumnasConsulta = len(resultadoConsulta[0])
        
        json = "["
        
        for fila in range(0, nFilasConsulta, 1):
            json += "\n\t{"
            
            for columna in range(0, nColumnasConsulta, 1):
                casilla = str(resultadoConsulta[fila][columna])
                json += "\n\t\t\"" + listaColumnasConsulta[columna] + "\": "
                if casilla == "nan":
                    json += "\"\""
                else:
                    if self._isNumero(casilla):  # HACER MÁS EFICIENTE: SE HACE PARA CADA ELEMENTO
                        json += casilla
                    else: 
                        json += "\"" + casilla + "\""
                    
                if columna != nColumnasConsulta-1:  # El último elemento de la columna no lleva coma.
                    json += ","
            json += "\n\t}"   
            if fila != nFilasConsulta-1:   # La última tupla no lleva coma.
                json += ","
        json += "\n]"
        
        print("\n\nFICHERO JSON:")
        print(json)
        
        file.write(json)
        file.close() 
        
    #Función "privada"    
    def _isNumero(self, s):
        """
        Comprueba si s es un número o no.

        PARAMETROS
        ----------
        s : string
            Cadena de texto a comprobar.

        RETURNS
        -------
        boolean: si s es un numero devuelve True, false en caso contrario.
        """
        # Expresión regular que determina un entero o double con o sin signo
        pattern = '((\+|-)?[0-9]+((\.|,)[0-9]+)?)'
        comprobacion = re.fullmatch(pattern, s)
        if comprobacion: 
            return True
        else:    
            return False  
    