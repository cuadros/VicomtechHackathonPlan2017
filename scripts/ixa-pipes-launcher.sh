# Descargar ixa-pipes1.1.1
## Server

java -jar ixa-pipe-tok-1.8.5-exec.jar server -l es -p 5001
java -jar ixa-pipe-pos-1.5.1-exec.jar server -l es -p 5002 -m morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin -lm morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin
java -jar ixa-pipe-nerc-1.6.1-exec.jar server -p 5003 -l es -m nerc-models-1.6.1/es/es-6-class-clusters-ancora.bin --dictTag post --dictPath ~/time.txt
## Client

#tok
echo "Holaaa" |java -jar ixa-pipe-tok-1.8.5-exec.jar client -p 5001
#pos
echo "Avui es el dia que fara Barcelona" |java -jar ixa-pipe-tok-1.8.5-exec.jar client -p 5001| java -jar ixa-pipe-pos-1.5.1-exec.jar client -p 5002
#ner
echo "Jordi Pujol viajo a Barcelona el año que viene, pasado mañana iremos a la playa con mi prima montse" |java -jar ixa-pipe-tok-1.8.5-exec.jar client -p 5001| java -jar ixa-pipe-pos-1.5.1-exec.jar client -p 5002| java -jar ixa-pipe-nerc-1.6.1-exec.jar client -p 5003


### mongoDB


create db mongoDB
mkdir /nlp/soft/hackathon/dataset_eventos
mongod --dbpath /nlp/soft/hackathon/dataset_eventos

mongoimport -d kulturklik -c events --file ~/Downloads/events_dump.json

## actualizar drop

mongoimport -d kulturklik -c events --file ~/Downloads/events_dump.json --drop

### java project de Aitor
mvn package
java -jar target/nlp...

Swagger veure serveis
localhost:8080/swagger.ui.html
