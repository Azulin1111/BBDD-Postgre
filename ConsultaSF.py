# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 17:47:34 2021

@author: Usuario
"""

from Consulta import Consulta

class ConsultaSF(Consulta):
    
    def __init__(self, nombreFicheroSalida="", tipoFicheroSalida=""):
        Consulta.__init__(self, nombreFicheroSalida, tipoFicheroSalida)
        
    def _formatoConsulta(self, selectLista, tabla, condicion):
        """
        Genera el string de una consulta tipo SELECT-FROM (no hay condición)
        
        Consulta básica en la base de datos del tipo:
            SELECT "id", "dc:identifier", "geo:long", "geo:lat"
            FROM callejero_edificiosmunicipales
        
        El formato será el siguiente:
            SELECT selectLista
            FROM tabla

        PARAMETROS
        ----------
        selectList : lista string
            Nombre de las columnas de salida en la consulta.
        tabla: string
            Nombre de la tabla que se consulta.

        RETURN
        -------
        String de la consulta.

        """
        consulta = "SELECT "
        consulta += "\"" + selectLista[0] + "\""
        for i in range(1, len(selectLista), 1):
            consulta += ", \"" + selectLista[i] + "\""
        consulta += "\nFROM \"" + tabla + "\""
        return consulta