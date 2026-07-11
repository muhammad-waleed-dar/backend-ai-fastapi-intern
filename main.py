from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, this is Waleed's backend!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
