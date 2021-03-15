# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 18:59:10 2021

@author: Usuario
"""
import re

def isNumero(s):
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
            print(s, "es un numero")
            return True
        else:    
            print(s, "no es un número")
            return False            
 