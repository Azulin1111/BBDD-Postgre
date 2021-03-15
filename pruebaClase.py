# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 17:12:13 2021

@author: Usuario
"""

from ControladorBD import ControladorBD

controlador = ControladorBD("localhost", "postgres", "postgres", "123456789")


#controlador.convertCSVtoBD("sorteo_casa_nino", r"sorteo_casa_nino.csv")


tiposInfo = ['aeropuertos', 'espacios-naturales', 'playas',
            'agencias-de-viajes', 'estaciones-de-autobus', 'plazas-de-toros',
            'albergues', 'estaciones-de-tren', 'puertos-deportivos',
            'alojamientos-vacacionales', 'estaciones-nauticas', 'recintos-feriales',
            'apartamentos-turisticos', 'festivales', 'restaurantes',
            'arte-rupestre', '_estas', 'spas',
            'balnearios', 'guias-de-turismo', 'taxis',
            'bodegas', 'hospederias-rurales', 'teatros',
            'Campings', 'hotel-apartamento', 'turismo-activo',
            'campos-de-golf', 'hoteles',
            'casas-rurales', 'mercadillos',
            'casinos', 'monumentos',
            'centros-comerciales', 'museos',
            'centros-de-artesania', 'o_cinas-de-congresos',
            'centros-de-congresos', 'o_cinas-de-turismo',
            'centros-de-interpretacion', 'organizadores-profesionales-de-congresos',
            'centros-de-talasoterapia', 'otros-ocio-y-diversion',
            'complejos-turisticos', 'parques-y-espacios-tematicos',
            'cursos-de-espa~nol', 'pensiones']

for tipo in tiposInfo:
    print("TABLA ", tipo)
    controlador.deleteTabla(tipo)
    if controlador.newConvertHTMLtoBD(tipo, tipo, "Cartagena"):  # Si es False es que no se ha añadido la información
        ficheroSalida = "salida" + tipo
        controlador.consultar(tipo, "", "", ficheroSalida, "json")

"""
tabla = "turismo-activo"
controlador.newConvertHTMLtoBD(tabla, tabla, "Cartagena")
"""
controlador.cerrarBD()





