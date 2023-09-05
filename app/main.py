import os
from typing import Optional

import jwt
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY", "myrefreshsecretkey")

templates = Jinja2Templates(directory="templates")

USER_DB = {
    "username1": "password1",
    "username2": "password2",
}


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


@app.post("/token")
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    if (
        form_data.username not in USER_DB
        or USER_DB[form_data.username] != form_data.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(data={"sub": form_data.username})
    response.set_cookie(key="token", value=access_token)
    return templates.TemplateResponse(
        "index.html", {"username": form_data.username, "request": {}}
    )


@app.get("/login", response_class=HTMLResponse)
def login_form():
    return templates.TemplateResponse("login.html", {"request": {}})


@app.get("/")
def get_cookie(token: Optional[str] = Cookie(None)):
    if not token:
        return RedirectResponse(url="/login", status_code=302)
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    username = payload.get("sub")
    if username not in USER_DB:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        "index.html", {"username": username, "request": {}}
    )
