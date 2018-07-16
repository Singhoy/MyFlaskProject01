from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import app, db

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    manager.run()
