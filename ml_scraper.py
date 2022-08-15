#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web scraping de Mercado Libre con Selenium Web Driver

Página de producto

** ACLARACIÓN: El siguiente script tiene un fin meramente educativo. No busca inflingir ninguna normativa. **

"""
# IMPORTAR LIBRERÍAS

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# ABRIR CHROME DRIVER Y DEFINIR PÁGINA A SCRAPEAR

website = "https://www.mercadolibre.com.ar/"

PATH = "/Users/ezequielpolacco/Downloads/chromedriver 2"

driver = webdriver.Chrome(PATH)

driver.get(website)

# PRODUCTO A BUSCAR
producto_buscar = 'molinillo cafe manual' 

# COOKIE ACCEPT
cookie_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cookie-consent-banner-opt-out__action.cookie-consent-banner-opt-out__action--primary.cookie-consent-banner-opt-out__action--key-accept')))
cookie_btn.click()

# INTRODUCIMOS ELEMENTO A BUSCAR
buscar = driver.find_element_by_class_name('nav-search-input').send_keys(producto_buscar)

# CLICK EN LUPITA BUSCAR
buscar_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nav-icon-search')))
buscar_btn.click()

# CLICK EN CLOSE X

aviso_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.andes-tooltip-button-close')))
aviso_btn.click()

# SET DE OPCIONES Y FILTROS
# CONDICIÓN = NUEVO
#condicion = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/aside/form/div[4]/ul/li[1]/button/span[1]') # Nuevo
#condicion.click()                         

# UBICACIÓN = CAPITAL FEDERAL
#ubicacion = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/aside/form/div[4]/ul/li[1]/button/span[1]') # Capital Federal
#ubicacion.click()


# PAGINACIÓN

total_paginas = driver.find_element_by_xpath('//li[@class="andes-pagination__page-count"]').text

productos = driver.find_elements_by_xpath('//li[@class="ui-search-layout__item"]')


link_list = []
condition = True

while condition:
    productos = driver.find_elements_by_xpath('//li[@class="ui-search-layout__item"]')
    for producto in productos:
        link = producto.find_element_by_class_name('ui-search-result__image').find_element_by_tag_name('a').get_attribute('href')
        link_list.append(link)
    try:
        driver.find_elements_by_class_name('andes-pagination__button.andes-pagination__button--next')[-1].click()
        
    except:
        condition = False


try:   # UTILIZO "TRY" EN CASO DE QUE NO ENCUENTRE LA PÁGINA, ENTONCES GUARDE LA INFO CONSEGUIDA HASTA ESE MOMENTO.
    
    #BUCLE FOR PARA INGRESAR EN CADA LINK Y SCRAPEAR LA INFO
    
    articulo_list = []
        
    for link in link_list:
        
        driver.get(url=link)  # get one book url
    
        # NOMBRE DEL ARTÍCULO
        
        nombre_art = driver.find_element_by_xpath('//h1[@class="ui-pdp-title"]').text
        
        # POSICIÓN ENTRE LOS MÁS VENDIDOS
        try:
            pos_mas_vendidos = driver.find_element_by_xpath('//*[@id="root-app"]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div/div[2]/a').text   
        except:
            pos_mas_vendidos = None
        
        # PRECIO
        precio = driver.find_element_by_xpath('//div[@class="ui-pdp-container__col col-2 ui-vip-core-container--short-description ui-vip-core-container--column__right"]//span[contains(text(), "$")]/following-sibling::span[1][1]').text
            
        # CUANDO LLEGA
        try:
            cuando_llega = driver.find_element_by_xpath('//div[@class="ui-pdp-container__col col-2 ui-vip-core-container--short-description ui-vip-core-container--column__right"]/div[@class="ui-pdp-container__row ui-pdp-container__row--shipping-summary"]/div[1]').text
        except:
            cuando_llega = "Info no disponible"
        
        # DEVOLUCIÓN GRATIS
        try:
            devolucion_gratis = driver.find_element_by_xpath('//p[@class="ui-pdp-color--GRAY ui-pdp-family--REGULAR ui-pdp-media__text"]').text
        except:
            devolucion_gratis = "Info no disponible"
        
        # CARACTERÍSTICA #1                                                 
        try:
            feature_1 = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/ul[1]/li[1]/p').text                                           
        except:
            feature_1 = None
        
        # CARACTERÍSTICA #2
        try:
            feature_2 = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/ul[1]/li[2]/p').text
        except:
            feature_2 = None
             
        # CARACTERÍSTICA #3     
        try:
            feature_3 = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/ul[2]/li[1]/p').text
        except:
            feature_3 = None
            
        # CARACTERÍSTICA #4    
        try:
            feature_4 = driver.find_element_by_xpath('/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/ul[2]/li[2]/p').text
        except:
            feature_4 = None
        
        # TOTAL OPINIONES
        try:
            total_opiniones = driver.find_element_by_xpath('//span[@class="ui-pdp-review__amount"]').text    
        except:
            total_opiniones = None
        
        # PROMEDIO OPINIONES
        try:
            promedio_opiniones = driver.find_element_by_xpath('//p[@class="ui-pdp-reviews__rating__summary__average"]').text
            
        except:
            promedio_opiniones = None
            
        # CANTIDAD DE ARTÍCULOS VENDIDOS   
        vendidos = driver.find_element_by_xpath('//span[@class="ui-pdp-subtitle"]').text
          
        # COLOR
        try:
            color = driver.find_element_by_xpath('//p[@class="ui-pdp-variations__label.ui-pdp-variations__label-only-text ui-pdp-color--BLACK"]').text
        except: 
            color = None
                
        # STOCK
        try:
            in_stock = driver.find_element_by_xpath('//div[@class="ui-pdp-buybox__quantity"]').text
        except:
            in_stock = driver.find_element_by_xpath('//span[@class="ui-pdp-buybox__quantity__available"]').text
        else:
            in_stock = '1 unidad disponible'
    
    
        # DICCIONARIO DONDE GUARDAMOS LA INFORMACIÓN RELEVADA
        articulos_item = {         
            "NOMBRE": nombre_art,
            "POSICIÓN MÁS VENDIDOS": pos_mas_vendidos,
            "PRECIO" : precio,
            "CUANDO LLEGA" : cuando_llega,
            "DEVOLUCIÓN" : devolucion_gratis,
            "ATRIBUTO 1" : feature_1,
            "ATRIBUTO 2" : feature_2,
            "ATRIBUTO 3" : feature_3, 
            "ATRIBUTO 4" : feature_4,
            "TOTAL OPINIONES" : total_opiniones, 
            "PROMEDIO OPINIONES" : promedio_opiniones,
            "UNIDADES VENDIDAS" : vendidos,
            "COLOR" : color,
            "EN STOCK" : in_stock
            
            }
        
        articulo_list.append(articulos_item)
        # CREACIÓN DE DATAFRAME Y GUARDADO COMO ARCHIVO .CSV PARA POSTERIOR USO
        df = pd.DataFrame(articulo_list)
        df.to_csv("definitivo2.csv", index=False)
        print(df)
    
    
    
except: NoSuchElementException("Ha ocurrido un error.")

finally:    
    print("Ejecución terminada")
    driver.quit()