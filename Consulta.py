# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:46:51 2021

@author: Usuario
"""
from abc import ABC, abstractmethod
from GeneradorJSON import GeneradorJSON
from GeneradorSinSalida import GeneradorSinSalida


# Al heredar una clase de la clase ABC, se convierte en abstracta
class Consulta(ABC):
    """
    Clase abstracta que representa una consulta a la base de datos
    """
    
    @abstractmethod
    def __init__(self, nombreFicheroSalida="", tipoFicheroSalida=""):
        """
        Consulta a la base de datos
        Si no se indican nombre de fichero de salida o su tipo, no se generará fichero de salida y se imprimirá por la salida estándar la consulta.  

        PARÁMETROS
        ----------
        nombreFicheroSalida (opcional) : string
            Nombre del fichero de salida.
        tipoFicheroSalida (opcional) : string
            Tipo del fichero de salida.

        RETURNS
        -------
        None.

        """
        self.generadorFichero = None
        self.nombreFicheroSalida = nombreFicheroSalida
        self.tipoFicheroSalida = tipoFicheroSalida
            
        if nombreFicheroSalida != "" and tipoFicheroSalida != "":
            self.tipoFicheroSalida = tipoFicheroSalida.upper()
            self.generadorFichero = self._generar()
            
        else: 
            self.generadorFichero = eval("GeneradorSinSalida()")
        
    
    def _generar(self):
        """
        Crea una instancia de la clase generador concreta que permite generar el tipo de fichero pedido.


        RETURNS
        -------
        Instancia de la clase generador concreta.

        """
        # Se va a crear una instancia de la clase concreta que genera el tipo concreto
        tipoFichero = self.tipoFicheroSalida #TODO no sé si habrá que hacer cambios o añadir casos
        nombreClase = "Generador" + tipoFichero
        
        # Función eval(): ejecuta lo que haya en el paréntesis
        try:
            return eval(nombreClase + '()')
        except NameError:
            return eval("GeneradorSinSalida()")
    
    
    def realizarConsulta(self, tabla, selectLista,  condicion, cur): # Método plantilla
        """
        Realiza una consulta en la base de datos.
            
        Las columnas si tienen un número serán tipo NUMERIC. En caso contrario, TEXT.
        
        PARAMETROS
        ----------
        selectList : lista string
            Nombre de las columnas de salida en la consulta.
        tabla: string
            Nombre de la tabla que se consulta.
        condicion: string
            Condiciones que debe cumplir la consulta.
        cur: cursor
            Cursor que accede a la base de datos

        RETURNS
        -------
        None.

        """
        
        # Decisión de diseño: hay que pasar cada uno de los parámetros para que no se pueda alterar la BD
        # Se obtiene el formato de la consulta a partir de la clase hija que la implemente.
        consulta = self._formatoConsulta(selectLista, tabla, condicion)
        cur.execute(consulta)
        resultadoConsulta = cur.fetchall()  # El resultado es una lista de tuplas
            
        self.generadorFichero.generar(resultadoConsulta, selectLista, self.nombreFicheroSalida)
        
    
    @abstractmethod
    def _formatoConsulta(self, selectLista, tabla, condicion):
        """
        Genera el string de la consulta.

        PARAMETROS
        ----------
        selectList : lista string
            Nombre de las columnas de salida en la consulta.
        tabla: string
            Nombre de la tabla que se consulta.
        condicion: string
            Condiciones que debe cumplir la consulta.

        RETURN
        -------
        String de la consulta.

        """
        pass
        
        
        