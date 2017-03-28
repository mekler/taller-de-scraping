#usar python3

#esquina inferior
#(10.948858, -119.307721)
#(-13281274.749425951, 1875584.389432249)
#
#esquina superior
#(31.907455, -84.824282)
#(-9442595.879145041, 3751168.7788644973)
import pycurl, pprint, time, json, sys
from io import BytesIO


def pideURL(url,cookie=False,cookie_name='cookie.txt', contador_curl = 0):
    time.sleep(2)
    
    print ("\n"+url+"\n")
    c = pycurl.Curl()
    if cookie:
        c.setopt(pycurl.COOKIEJAR, 'cookies/'+cookie_name)
        c.setopt(pycurl.COOKIEFILE, 'cookies/'+cookie_name)
    c.setopt(pycurl.URL, url)       
    c.setopt(pycurl.CONNECTTIMEOUT, 15) 
    c.setopt(pycurl.TIMEOUT, 25) 
    c.setopt(pycurl.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,'Accept-Language: en-US,en;q=0.5' ,'Connection: keep-alive' ,'Content-Type: application/x-www-form-urlencoded' ,'Host: services6.arcgis.com' ,'Origin: https://sig-ruv.maps.arcgis.com' ,'Referer: https://sig-ruv.maps.arcgis.com/apps/webappviewer/index.html?id=1e3873d1c01749929457c7a7b9315cda'])
    #c.setopt(pycurl.VERBOSE, 1)
   
    b = BytesIO()
    BytesIO
    c.setopt(pycurl.WRITEFUNCTION, b.write)

    try:
        c.perform()
        return b.getvalue()
        #print (response_string)
        b.close()
    except Exception as e:
        #log ('Razon:',e)
        response_string = None
        if contador_curl<=10:
            time.sleep(5)
            pideURL(url,contador_curl+1)
        else:
            print ('Error: ',url)
            print ('Error log: ',e)


def regresaCuadricula(puntoInferior, puntoSuperior, papa="0",depth = 0):
    print (puntoInferior,puntoSuperior)
    cuadros= []
    xprom = (puntoInferior['x']+puntoSuperior['x'])/2
    yprom = (puntoInferior['y']+puntoSuperior['y'])/2
    #cuadrante1
    cuadros.append( ({'x':puntoInferior['x'],'y':yprom}, {'x':xprom,'y':puntoSuperior['y']}) )

    #cuadrante2
    cuadros.append( ({'x':xprom,'y':yprom}, puntoSuperior) )

    #cuadrante3
    #cuadros.append( (puntoInferior, infCuadro2) )
    cuadros.append( (puntoInferior, cuadros[1][0]) )

    #cuadrante4
    cuadros.append( ({'x':xprom,'y':puntoInferior['y']}, {'x':puntoSuperior['x'],'y':yprom}) )

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(cuadros)

    i = 1
    for coordenadas in cuadros:
        url = 'http://argis-prod-sds.cloudapp.net:6080/arcgis/rest/services/SIG_BETA/SIG_RUV_4/MapServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{}%2C%22ymin%22%3A{}%2C%22xmax%22%3A{}%2C%22ymax%22%3A{}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile'.format(
               #http://argis-prod-sds.cloudapp.net:6080/arcgis/rest/services/SIG_BETA/SIG_RUV_4/MapServer/export?dpi=96&transparent=true&format=png32&layers=show%3A-1%2C-1%2C-1%2C0&bbox=-9392582.035679959%2C1409823.6865701713%2C9392582.03567996%2C6556175.92695315&bboxSR=%7B%22wkt%22%3A%22PROJCS%5B%5C%22WGS_1984_Web_Mercator_Auxiliary_Sphere%5C%22%2CGEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2CSPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137.0%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Mercator_Auxiliary_Sphere%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-105.7560781249972%5D%2CPARAMETER%5B%5C%22Standard_Parallel_1%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Auxiliary_Sphere_Type%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Meter%5C%22%2C1.0%5D%5D%22%7D&imageSR=%7B%22wkt%22%3A%22PROJCS%5B%5C%22WGS_1984_Web_Mercator_Auxiliary_Sphere%5C%22%2CGEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2CSPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137.0%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Mercator_Auxiliary_Sphere%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-105.7560781249972%5D%2CPARAMETER%5B%5C%22Standard_Parallel_1%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Auxiliary_Sphere_Type%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Meter%5C%22%2C1.0%5D%5D%22%7D&size=1920%2C526&f=image
                coordenadas[0]['x'],
                coordenadas[0]['y'],
                coordenadas[1]['x'],
                coordenadas[1]['y']
            )
        respuesta = pideURL(url)
        try:
            jason = json.loads(respuesta.decode('utf-8'))
            if len(jason['features']) == 8000:
                regresaCuadricula(coordenadas[0], coordenadas[1], papa+str(i),depth +1)
            else:
                with open('jasones/cuadro{}-{}-{}.json'.format(papa,i,depth), 'w') as outfile:
                    json.dump(jason, outfile)
        except Exception as e:
            print (e)
        i = i + 1





regresaCuadricula({'x':-13281274.749425951, 'y':1875584.389432249},{'x':-9442595.879145041, 'y':3751168.7788644973})