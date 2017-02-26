nohup java -jar ixa-pipe-tok-1.8.5-exec.jar server -l es -p 5001&
nohup java -jar ixa-pipe-pos-1.5.1-exec.jar server -l es -p 5002 -m morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin -lm morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin&
nohup java -jar ixa-pipe-nerc-1.6.1-exec.jar server -p 5003 -l es -m nerc-models-1.6.1/es/es-clusters-dictlbj-conll02.bin --dictTag post --dictPath ../nerc-data/dictionaries/ &
