import os

from chat.controller.routes import app
print("teste de proteção endpoint")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)
