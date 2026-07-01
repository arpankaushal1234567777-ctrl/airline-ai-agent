from fastapi import FastAPI

app = FastAPI(
    title="Airline AI Agent",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Airline AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}