from fastapi import FastAPI

from app.routers import auth, user, table

app = FastAPI()


app.include_router(table.router)
app.include_router(auth.router)
app.include_router(user.router)
