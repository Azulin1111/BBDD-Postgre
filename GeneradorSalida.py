# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:50:10 2021

@author: Usuario
"""
from abc import ABC, abstractmethod


class GeneradorSalida(ABC):
    """
    Interfaz que permite obtener un fichero de salida concreto a partir de una consulta
    """
    
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def generar(self, resultadoConsulta, listaColumnasConsulta, nombreFicheroSalida):
        """
        Genera un formato determinado para una consulta.

        PARÁMETROS
        ----------
        resultadoConsulta : string
            Salida de la consulta a la base de datos.
        listaColumnasConsulta : lista de string
            Lista de las columnas pedida en la sentencia SELECT.
        nombreFicheroSalida: string
            Nombre del fichero .json que contendrá el resultado de la consulta. No incluir la terminación .json

        RETURN
        -------
        None.
        
        POSTCONDICIONES
        ---------------
        Genera fichero de salida con el formato adecuado en caso de que haya clase asociada que lo permita.

        """
        pass