from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import user, sessions, role, service, absence, program, asks, code, contrat, speciality, pole, saphir, availability, planning

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router,)
app.include_router(role.router)
app.include_router(absence.router)
app.include_router(program.router)
app.include_router(code.router)
app.include_router(asks.router)
app.include_router(service.router)
app.include_router(contrat.router)
app.include_router(speciality.router)
app.include_router(pole.router)
app.include_router(sessions.router)
app.include_router(saphir.router)
app.include_router(availability.router)
app.include_router(planning.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
