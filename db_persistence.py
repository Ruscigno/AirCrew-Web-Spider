from pymongo import MongoClient

def inserirQuestao(questao):
    cliente = MongoClient()
    banco = cliente.aircrew
    collection = banco.questoes
    rec = collection.find_one({'course':questao['course'],'group':questao['group'],'questao':questao['questao']})
    if rec is None:
        collection.insert_one(questao)

def inserirQuestoes(questoes):
    cliente = MongoClient()
    banco = cliente.aircrew
    collection = banco.questoes
    for questao in questoes:
        rec = collection.find_one({'course':questao['course'],'group':questao['group'],'questao':questao['questao']})
        if rec is None:
            collection.insert_one(questao)
        #else:
            #print("Original:", questao, "\n", "Novo:", rec)