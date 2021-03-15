# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:06:39 2021

@author: Usuario
"""
from Consulta import Consulta

class ConsultaSFW(Consulta):
    
    def __init__(self, nombreFicheroSalida="", tipoFicheroSalida=""):
        Consulta.__init__(self, nombreFicheroSalida, tipoFicheroSalida)
        
    def _formatoConsulta(self, selectLista, tabla, condicion):
        """
        Genera el string de una consulta tipo SELECT-FROM-WHERE.
        
        Consulta básica en la base de datos del tipo:
            SELECT "id", "dc:identifier", "geo:long", "geo:lat"
            FROM callejero_edificiosmunicipales
            WHERE "dc:identifier"=1555 OR "dc:identifier"=1222;
        
        El formato será el siguiente:
            SELECT selectLista
            FROM tabla
            WHERE condicion;

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
        consulta = "SELECT "
        consulta += "\"" + selectLista[0] + "\""
        for i in range(1, len(selectLista), 1):
            consulta += ", \"" + selectLista[i] + "\""
        consulta += "\nFROM \"" + tabla + "\""
        consulta += "\nWHERE " + condicion + ";"
        
        return consulta