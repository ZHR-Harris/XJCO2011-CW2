from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from exts import db
from models import User

manager = Manager(app)

# use Migrate to bind app and db
migrate = Migrate(app, db)

# add migrate srcipts command to manager
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()