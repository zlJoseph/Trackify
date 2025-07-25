from fastapi import FastAPI
from interfaces.http.routes import users, auth
from interfaces.http.exception_registry import handle_known_exceptions

app = FastAPI(title="Trackify API")
app.add_exception_handler(Exception, handle_known_exceptions)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
