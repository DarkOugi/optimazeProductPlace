# import Apriori
# transactions = [
#     {'молоко', 'хлеб', 'масло'},
#     {'хлеб', 'масло'},
#     {'молоко', 'хлеб', 'масло', 'сыр'},
#     {'хлеб', 'сыр'},
#     {'молоко', 'хлеб', 'сыр'}
# ]
#
# a = Apriori.Apriori(1)
# a.Train(transactions)
# print(a.get_info())


import uvicorn
from fastapi import FastAPI
from Back.Models import Place
import Algo.Data as data
import Algo.PreProcessing as convert
import Algo.Store as store
import Algo.Apriori.Apriori as apriori

app = FastAPI()


@app.get("/new_place")
async def get_new_product_place(ml : Place):
    tr = data.Transaction(*ml.dates)
    tr = tr.get_dataset()
    transactions = convert.Preprocessing(tr,'sql')
    if not ml.model or ml.model == 'apriori':
        a = apriori.Apriori()
        a.Train(transactions)
        return {"result": a.get_info()}
    else:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
