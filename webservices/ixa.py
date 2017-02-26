# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin

from lxml import etree
import os
import sys
from subprocess import Popen, PIPE
import re
import codecs
import json


#informacion: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask



app = Flask(__name__)

CORS(app)



@app.route('/analyze', methods=['POST'])

def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    else:
        return parse_file(request.json['title'])



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def parse_file(document):
#    text = "Hola me ll Naiara Perez y vivo en Donostia. Naiara Perez es muy majo. Quiero ir a un Concierto a Barcelona pasado mañana."
    naf = full_parse(document.encode("utf-8"))
    root = etree.fromstring(naf)
    result = get_json(root)
    #print result
    return result
#    print "Parsing Document"

#    proba={}
#    proba['content']="montse"

#    json_data=json.dumps(data)

#    json_data=json.dumps(proba)
#    return json_data

########################################################################################################################
####################################### IXA PIPES PATHS TO BE CONFIGURED!! #############################################

IXA_HOME = '/Users/nuriona/Documents/Montse/vicomnlphackathonplan/ixa-pipes-1.1.1'

TOK_PORT = 5001
POS_PORT = 5002
NERC_PORT = 5003

TOKENIZER_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-tok-1.8.5-exec.jar'), 'client', '-p', str(TOK_PORT)]
TAGGER_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-pos-1.5.1-exec.jar'), 'client', '-p', str(POS_PORT)]
NERC_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-nerc-1.6.1-exec.jar'), 'client', '-p', str(NERC_PORT)]

# TOKENIZER_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-tok-1.8.5-exec.jar'), 'client', '-p', str(TOK_PORT)]
# TAGGER_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-pos-1.5.0.jar'), 'client', '-p', str(POS_PORT)]
# NERC_CMD = ['java', '-jar', os.path.join(IXA_HOME, 'ixa-pipe-nerc-1.6.0-exec.jar'), 'client', '-p', str(NERC_PORT)]

########################################################################################################################
##############################    NAF DOCUMENT TAG CONSTANTS - DO NOT CHANGE    ########################################

# Text layer
TEXT_LAYER_TAG = "text"

# Term layer
TERM_ID_CHAR = "t"
TERM_ID_CHAR_LEN = len(TERM_ID_CHAR)

# Named entity layer in NAF
NAMED_ENTITIES_LAYER_TAG = "entities"
NAMED_ENTITY_OCCURRENCE_TAG = "entity"
NAMED_ENTITY_TYPE_ATTRIBUTE = "type"
NAMED_ENTITY_REFERENCES_GROUP_TAG = "references"

# References tags
SPAN_TAG = "span"
TARGET_ID_ATTRIBUTE = "id"
TARGET_TAG = "target"

########################################################################################################################
########################################################################################################################

def get_json_complete(naf_root):
    """
    Given the xml root of a NAF document with the entities layer, this function returns a json string with two main
    entries: the tokens of the NAF as a list, and the NE by type and position of the spans, like so:

    {"tokens": ["Hola", "me", "llamo", "Naiara", "Perez", "y", "vivo", "en", "Donostia", "."],
     "nerc": {"ORG": [[0], [3, 4]], "LOC": [[8]]}}

    :param naf_root: root element of the NAF document
    :return: json string
    """
    dico = {}

    # Get the wordform list
    dico["tokens"] = [tok_ele.text for tok_ele in naf_root.find(TEXT_LAYER_TAG)[:]]

    # Get the named entities dictionary
    nerc = {}
    ne_elements = naf_root.findall("{0}/{1}".format(NAMED_ENTITIES_LAYER_TAG, NAMED_ENTITY_OCCURRENCE_TAG))
    for ne_ele in ne_elements:
        type = ne_ele.get(NAMED_ENTITY_TYPE_ATTRIBUTE)
        ref_elements = ne_ele.findall("{0}/{1}/{2}".format(NAMED_ENTITY_REFERENCES_GROUP_TAG, SPAN_TAG, TARGET_TAG))
        references = []
        for ref_ele in ref_elements:
            idx = int(ref_ele.get(TARGET_ID_ATTRIBUTE)[TERM_ID_CHAR_LEN:]) - 1
            references.append(idx)
        if type not in nerc.keys():
            nerc[type] = []
        nerc[type].append(references)
    dico["nerc"] = nerc

    return json.dumps(dico)


def get_json(naf_root):
    """
    Given the xml root of a NAF document with the entities layer, this function returns a json string with the NE by
    type and the span tokens, like so:

    {"ORG": [["Hola"]], "PER": [["Naiara", "Perez"]], "LOC": [["Donostia"]]}

    :param naf_root: root element of the NAF document
    :return: json string
    """

    # Get the wordform list
    tokens = [tok_ele.text for tok_ele in naf_root.find(TEXT_LAYER_TAG)[:]]

    # Get the named entitities dictionary (keys are NE types)
    nerc = {}
    ne_elements = naf_root.findall("{0}/{1}".format(NAMED_ENTITIES_LAYER_TAG, NAMED_ENTITY_OCCURRENCE_TAG))
    for ne_ele in ne_elements:
        type = ne_ele.get(NAMED_ENTITY_TYPE_ATTRIBUTE).lower()
        ref_elements = ne_ele.findall("{0}/{1}/{2}".format(NAMED_ENTITY_REFERENCES_GROUP_TAG, SPAN_TAG, TARGET_TAG))
        references = ""
        for ref_ele in ref_elements:
            idx = int(ref_ele.get(TARGET_ID_ATTRIBUTE)[TERM_ID_CHAR_LEN:]) - 1
            references=references+" "+tokens[idx]
        if type not in nerc.keys():
            nerc[type] = ""
        if not nerc[type]:
                nerc[type]=references.strip()
        else:
            nerc[type]=nerc[type]+","+references.strip()

    return json.dumps([nerc])


def full_parse(text):
    """
    Obtain NAF annotation of Named entities given a text string
    :param text: string to parse
    :return: NAF string with named entity annotations added (entities layer)
    """
    return nerc(tag(tokenize(text)))


def tokenize(text):
    """
    Obtain NAF annotation of tokens given a text string
    :param text: text to be analyzed
    :return: NAF string resulting from the parse
    """
    return call_terminal(TOKENIZER_CMD, text)


def tag(naf_string):
    """
    Obtain NAF annotation of morphological features given a NAF with token annotations
    :param naf_string: NAF with token annotations (text layer)
    :return: NAF string with morphological annotations added (terms layer)
    """
    return  call_terminal(TAGGER_CMD, naf_string)


def nerc(naf_string):
    """
    Obtain NAF annotation of Named entities given a NAF with morphological annotations
    :param naf_string: NAF with terms layer
    :return: NAF string with named entity annotations added (entities layer)
    """
    return  call_terminal(NERC_CMD, naf_string)


def call_terminal(cmd, input_str):
    """
    Function to call IXA-pipes annotation tools
    :param cmd: command to call the tool; these should be specified at the top of this module
    :param input_str: input to the call (either a text to tokenize, or a NAF string for other annotations)
    :return: NAF annotation as string
    """
    try:
        call = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        call.stdin.write(input_str)
        call.stdin.close()
        error = call.stderr.read()
        response = call.stdout.read()
        if "Error" in error or "Exception" in error:
            raise Exception(error)
        return response
    except Exception as e:
        print "There was an error upon calling '{0}': {1}".format(" ".join(cmd), e)
        raise Exception

if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5065, debug=True)
