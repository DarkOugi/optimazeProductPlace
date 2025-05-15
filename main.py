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

app = FastAPI()


@app.get("/new_place")
async def get_new_product_place(ml : Place):

    return {"q": ml }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
