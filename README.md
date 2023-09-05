# jwt-fastapi

JWT+FastAPIのサンプルサーバを構築

JWT認証でトークンを発行し認証(もどき)を実装する

厳密ではないが，Cookie情報をもとにユーザの認証を行う

Cookieがない場合はログイン画面へリダイレクトする

## setup

```sh
rye sync
```

or

```sh
pip install -r requirements.lock
```

## how to

```sh
rye run uvicorn main:app --reload --port 9000
```

## フォルダ構成

```sh
.
├── README.md
├── app
│   ├── main.py
│   └── templates
│       ├── index.html
│       └── login.html
├── pyproject.toml
├── requirements-dev.lock
└── requirements.lock
```