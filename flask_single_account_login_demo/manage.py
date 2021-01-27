from app import create_app
from app.extensions import db, socketio
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import User

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7771, debug=True)
