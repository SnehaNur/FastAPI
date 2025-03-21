from fastapi import FastAPI

app = FastAPI()

List = [
    {'name':'Hafsa','id':'202020','dep':'development'},
    {'name':'Hasib','id':'201120','dep':'development'},
    {'name':'Rubaiya','id':'332020','dep':'development'},
    {'name':'Rahim','id':'20202052','dep':'development'}
]

@app.get("/")
async def info()-> list[dict]:
    return List