from pymongo import MongoClient

def salvarQuestoes(questoes):
    print(questoes)
    cliente = MongoClient()
    banco = cliente.aircrew
    collection = banco.questoes
    post_id = collection.insert_many(questoes).inserted_id
    print(post_id)