from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Gateway is up and running'}
