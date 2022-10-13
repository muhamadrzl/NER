import json, os
# from ... import centralConfig as CFG

def handling_slangwords(teks):
    # pathSlangwords = os.path.join(CFG.CREATEMODELS_CHATBOT_PATH + "slangwords.json")
    pathSlangwords = 'slangwords.json'
    with open(pathSlangwords, 'r') as f:
            slangwords = json.load(f)

    test_string = teks

    # split the words based on whitespace
    sentence_list = test_string.split()

    # make a place where we can build our new sentence
    new_sentence = []

    # look through each word 
    for word in sentence_list:
        # print(word)
        # look for each candidate
        for candidate_replacement in slangwords:
            # if our candidate is there in the word
            if candidate_replacement == word:
                # print(candidate_replacement)
                # replace it 
                word = word.replace(candidate_replacement, slangwords[candidate_replacement])

        # and pop it onto a new list 
        new_sentence.append(word)

    message = " ".join(new_sentence)
    # print(message)
    return message