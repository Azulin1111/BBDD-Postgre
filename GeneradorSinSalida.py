# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 17:21:21 2021

@author: Usuario
"""
from GeneradorSalida import GeneradorSalida

class GeneradorSinSalida(GeneradorSalida):  # Patrón OBJETO NULL
                
    def __init__(self):
        """
        Esta clase representa la ausencia de generador de fichero de salida.

        Returns
        -------
        None.

        """
        GeneradorSalida.__init__(self)
    
    
    def generar(self, resultadoConsulta, listaColumnasConsulta, nombreFicheroSalida):
        """
        Imprime un mensaje indicando que no se ha creado ningún fichero de salida o se ha escrito mal su tipo.
        Ninguno de los parámetros es importante.
        
        PARAMETROS
        ----------
        resultadoConsulta : string
        listaColumnasConsulta : lista de string
        nombreFicheroSalida: string
           

        Returns
        -------
        None.

        """
        print("""No se ha creado ningún fichero de salida.\nRevise si se ha escrito bien el tipo de fichero de entrada.""")
        print("CONSULTA: ")
        print(resultadoConsulta)