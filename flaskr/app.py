from database import app, models
from blueprints.crud import crud

app.register_blueprint(crud)

@app.route('/')
def hello_world():
    users = models.User.query.all()
    return str(users[0])


print(app.url_map)
if __name__ == '__main__':
    app.run()
