#!/bin/bash 
# Carlos S. Pérez 
# IMSS scrapper

#Init Params
BOOL=0
COUNTER=1

#rm imss.txt
#Out File
touch imss.txt

## Main Looper
while [  $BOOL -lt 1 ]; do
	##POST curl
	str="$(curl --data "&type=compras&message=X&filtered=1&descripcion=&proveedor=&numcompra=&delegacion=values%3D&fecha=min%3D%3Bmax%3D&procedimiento=values%3D&exact=false&numperpage=20&page=1&order=fecha%20desc" http://buscador.compras.imss.gob.mx/index.php)"
	#echo "$str"
	## Continuity Condition 
	if [ ! -z "$str" ]; then
	    echo "PAGE $COUNTER Burned!" ##Success Message
	    echo "$str" >> imss.txt   ##Output append
	    let COUNTER=COUNTER+1    
	else
	    echo "Output is null"
	    echo "Total PAGS = $COUNTER"
	    BOOL=1 
	fi
done

##SANITY CHECK 
#Conteo total registros via campo 'clave'

cat imss.txt | grep -o 'clave' | wc -l