class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:24320919@127.0.0.1:3307/dsc_db'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    # SECRET_KEY = '24320919'