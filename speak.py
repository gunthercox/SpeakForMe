from flask import Flask
from views import Api


app = Flask(__name__)

app.add_url_rule("/", view_func=Api.as_view("api"))

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development"
    )
    app.run(host="0.0.0.0", port=8000)
