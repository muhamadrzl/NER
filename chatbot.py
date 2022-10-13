import os, json, random
from matplotlib.style import use
import torch
import spacy
from TextPreprocessing import textprocessing as tp
from stem import stemmer as st
# from ... import centralConfig as CFG
from slangword import handling_slangwords
from model import KnowledgeSys
from nltk_utilities import bag_of_words, tokenize

# from ... import centralConfig as CFG

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def get_response(username, msg):
    # knowledgePath = os.path.join(CFG.KNOWLEDGE_CHATBOT_PATH + username + '.json')
    knowledgePath = 'itsrizal.json'
    with open(knowledgePath, 'r') as f:
        intents = json.load(f)
    # modelsPath = os.path.join(CFG.MODELS_CHATBOT_PATH + username + ".pth")
    modelsPath = 'itsrizal.pth'
    data = torch.load(modelsPath)
    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    model = KnowledgeSys(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    msg = handling_slangwords(msg)
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intent']:
            if tag == intent['name']:
                return random.choice(intent['actions'])

    return "Maaf saya tidak mengerti."

def entity(sentence):
    nlp_ner = spacy.load("model-best")
    sentence = tp(sentence)
    doc = nlp_ner(sentence)
        # spacy.displacy.render(doc, style="ent", jupyter=False)
    a, b = [], []
    for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            text = st(ent.text)
            a.append(text)
            b.append(ent.label_)
    # a = tp(a)
    dictionary = dict(zip(b, a))
     # print(dictionary)
    app_json = json.dumps(dictionary)
    print(app_json)

if __name__ == "__main__":
    print("Selamat datang di sistem asisten chat Central AI. Ketik 'exit' untuk menutup chat")
    while True:
        sentence = input("You: ")
        if sentence == 'exit':
            break
        resp = get_response('rizal', sentence)
        entity(sentence)
        # print(resp)
