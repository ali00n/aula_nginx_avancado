import os

class Config:
    INSTANCE_ID = os.environ.get('INSTANCE_ID', 'backend-default')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))
