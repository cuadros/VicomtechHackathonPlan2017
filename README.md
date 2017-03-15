# Prototipo Vicomtech-IK4


Este repositorio contiene el código fuente desarrollado en el Primer Hackathon de PLN <http://www.primerhackathonpln.es/> del Plan de Impulso de las Tecnologías del Lenguaje. El contenido fue desarrollado por el equipo de Vicomtech-IK4 <http://www.vicomtech.org> compuesto por:

+ Montse Cuadros, Aitor García Pablos, Naiara Pérez y Manex Serras.

El protitpo presentado a partir de una petición relacionada con el interés de acudir a un evento cultural, proporciona el conjunto de eventos culturales futuros en euskadi. Los eventos son obtenidos a partir de OpenData Euskadi.
La búsqueda se puede ir refinando añadiendo localizaciones concretas y fechas concretas, y de forma dinámica el buscador encuentra los eventos relacionados. 

El prototipo usa tecnología de NLP para encontrar los eventos destacados en una frase, de IR para buscar eventos en una base de datos y finalmente la interfaz esta hecha en AngularIU. 

Las diferentes componentes que analizan el texto estan implementados como webservices. 

## Dependencias NLP

+ ixa-pipes-1.1.1 <http://ixa2.si.ehu.es/ixa-pipes/>

## Dependencias software

+ java8, maven3, python 2.7, angular2, mongodb

## Ejecución

Una vez descargado ixa-pipes-1.1.1 se deben poner los siguientes servicios en modo servidor:

```
nohup java -jar ixa-pipe-tok-1.8.5-exec.jar server -l es -p 5001&
nohup java -jar ixa-pipe-pos-1.5.1-exec.jar server -l es -p 5002 -m morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin -lm morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin&
nohup java -jar ixa-pipe-nerc-1.6.1-exec.jar server -p 5003 -l es -m nerc-models-1.6.1/es/es-clusters-dictlbj-conll02.bin --dictTag post --dictPath ../nerc-data/dictionaries/ &

```

Instalar mongodb para detectar eventos con los siguientes pasos:

```
mongoimport -d kulturklik -c events --file events_dump.json --drop
mongoimport -d kulturklik -c hotels --file hotels_dump.json --drop
mongoimport -d kulturklik -c restaurants --file restaurants_dump.json --drop

```
Compilar el proyecto nlp-hackathon:
```
mvn package
java -jar target/nlp-hackathon-0.0.1-SNAPSHOT.jar

```
En <localhost:8080/swagger.ui.html> se pueden ver los servicios de eventos


Lanzar los webservices para leer entidades y traducir las fechas

```
cd webservices
python ixa.py
python dates.py

```

Lanzar la interfaz grafica:

```
cd angularIU
ng serve
```


# Información de contacto

````shell
Montse Cuadros
Vicomtech-IK4
20009 Donostia-San Sebastián
mcuadros@vicomtech.org
````
