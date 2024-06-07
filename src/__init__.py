import os, secrets
from flask import Flask, request, session, redirect
from psycopg import Connection
from psycopg.rows import dict_row
from dotenv import load_dotenv

con = None

try:
    load_dotenv(".env")
    con = Connection.connect(
        host = os.getenv("POSTGRES_HOST"),
        port = os.getenv("POSTGRES_PORT"),
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")
    )
except Exception as e:
    exit(1)

def create_app():
    app = Flask(__name__)

    with open(os.getenv("FLASK_SECRET_PATH"), "r") as file:
        app.secret_key = file.read().strip()

    from src.routes.index import Index
    from src.routes.error import Error
    from src.routes.groups import Groups
    app.register_blueprint(Index)
    app.register_blueprint(Error)
    app.register_blueprint(Groups)

    locales = None
    with con.cursor(row_factory=dict_row) as cursor:
        locales = [row["locale"] for row in cursor.execute("SELECT * FROM locales;").fetchall()]

    @app.get("/locale/<iso>")
    def set_locale(iso: str):
        for row in locales:
            if row["id"] != iso:
                continue
            session["locale"] = row
            break
        if request:
            return redirect(request.referrer)

    @app.context_processor
    def inject_locale():
        if not "locale" in session:
            print("ehm")
            for row in locales:
                if row["id"] != "en_EN":
                    continue
                session["locale"] = row
                break
        return {"locale": session["locale"], "locales": locales}


    return app
