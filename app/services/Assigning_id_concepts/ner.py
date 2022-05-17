import torch
from transformers import BertTokenizer,BertForTokenClassification
import numpy as np
import json
from os import path

import nltk    
nltk.download('punkt')


def predictBERTNER(sentencas, MODEL_DIR):
    """ 
    function that calculates the NER for each 
    token of a given clinical note.

    Parameters
    ----------
    sentencas list: a list containing the clinical terms.

    MODEL_DIR str: biobert's model path.
    
    Return
    ------
    term_concept_id list: list containing all concepts
        found in snomed for the given term.
    """

    model = BertForTokenClassification.from_pretrained(MODEL_DIR)
    tokenizer = BertTokenizer.from_pretrained(MODEL_DIR, do_lower_case=True) # lower or not, this is important

    with open(MODEL_DIR + '/idx2tag.json', 'r') as filehandle:
        idx2tag = json.load(filehandle) 
        
    predictedModel=[]
    
    for test_sentence in sentencas:
        tokenized_sentence = tokenizer.encode(test_sentence)
        input_ids = torch.tensor([tokenized_sentence])#.cuda()
        
        with torch.no_grad():
            output = model(input_ids)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
        
        # join bpe split tokens
        tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        new_tokens, new_labels = [], []
        for token, label_idx in zip(tokens, label_indices[0]):
            if token.startswith("##"):
                new_tokens[-1] = new_tokens[-1] + token[2:]
            else:
                new_labels.append(label_idx)
                new_tokens.append(token)
            
        FinalLabelSentence = []
        for token, label in zip(new_tokens, new_labels):
            label = idx2tag[str(label)]
            if label == "O" or label == "X":
                FinalLabelSentence.append("O")
            else:
                FinalLabelSentence.append(label)
                
        predictedModel.append(FinalLabelSentence[1:-1]) # delete [SEP] and [CLS]
        
            
    return predictedModel