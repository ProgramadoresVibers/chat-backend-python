from controller.routes import app
print("teste de proteção endpoint")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)