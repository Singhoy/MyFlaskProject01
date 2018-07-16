from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import db, create_app

# 创建app，并传入配置模式：dev/pro
app = create_app('dev')

# 添加扩展命令行
manager = Manager(app)

# 数据库迁移
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
