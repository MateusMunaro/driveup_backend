from fastapi import FastAPI
from gateway import router as gateway_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(gateway_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)