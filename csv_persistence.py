import pandas as pd

def salvarQuestoes(questoes, file):
    db = pd.read_csv(file)
    print(db.size)
    new = {}
    if (db.size == 0):
        return
    else:
        for item in questoes:
            if not (db.loc[db['course'] == item['course'] & db['group'] == item['group'] & db['questao'] == item['questao']]):
                db.append(item)
    
    db.to_csv(db)