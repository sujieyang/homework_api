from flask import Flask
from flask_sqlalchemy import SQLAlchemy
class Config():
    ECRET_KEY = "asdasda"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/Workapi"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 40 * 1024 * 1024
    SQLALCHEMY_POOL_SIZE = 1024 # 连接池大小
    SQLALCHEMY_POOL_TIMEOUT = 90 # 池中没有线程最多等待的时间，否则报错
    SQLALCHEMY_POOL_RECYCLE = 3 # 多久之后对线程池中的线程进行一次连接的回收（重置）
    SQLALCHEMY_MAX_OVERFLOW = 1024 # 超过连接池大小外最多创建的连接

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Thing(db.Model):
    __tablename__ = "thing_info"
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer,nullable = False)
    addtime = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.String(255), nullable=False)

#db.create_all()
