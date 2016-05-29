#Scrapy y comandos básicos

####Crear proyecto
```
#scrapy startproject [nombre_del_proyecto]
#ejemplo

scrapy startproject mercadolibre
```

####Pruebas de búsquedas
```
#scrapy shell "[url_completo]"
#ejemplo
scrapy shell "http://www.mercadolibre.com.mx/"
```

####Correr una araña
```
#scrapy crawl [nombre_de_la_araña_definido_en_archivo_dentro_del_folder_spiders]
#Nota: tienen que estar dentro de la carpeta del proyecto
#ejemplo
scrapy crawl ml_crawler

```