# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 19:08:03 2021

@author: Usuario
"""

from Consulta import Consulta

class ConsultaTotal(Consulta):
    def __init__(self, nombreFicheroSalida="", tipoFicheroSalida=""):
        Consulta.__init__(self, nombreFicheroSalida, tipoFicheroSalida)
        
        
    def _formatoConsulta(self, selectLista, tabla, condicion):
        """
        Obtiene toda la tabla entera.
        
        Genera una consulta del tipo
            SELECT *
            FROM tabla
        
        PARÁMETROS
        ----------
        selectLista : string
            Campo vacío.
        tabla : string
            Nombre de la tabla a consultar.
        condicion : string
            Campo vacío.

        Returns
        -------
        None.

        """
        consulta = "SELECT *"
        consulta += "\nFROM \"" + tabla + "\""
        return consulta