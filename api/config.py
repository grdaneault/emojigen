import os


class Config(object):
    DATA_DIR = '/tmp/emojigen'
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDIS_CONNECTION_STR = ''

    def __init__(self):
        print('Configuring emojigen...')
        self.DATA_DIR = os.getenv('DATA_DIR', self.DATA_DIR)
        self.UPLOAD_FOLDER = os.path.join(self.DATA_DIR, 'uploads')
        self.GENERATED_FOLDER = os.path.join(self.DATA_DIR, 'generated')
        self.REDIS_HOST = os.getenv('REDIS_HOST', self.REDIS_HOST)
        self.REDIS_PORT = os.getenv('REDIS_PORT', self.REDIS_PORT)
        password = os.getenv('REDIS_PASSWORD', '')
        if password:
            password = f':{password}@'
        self.REDIS_CONNECTION_STR = os.getenv('REDIS_CONNECTION_STR', f'redis://{password}{self.REDIS_HOST}:{self.REDIS_PORT}')

        print(f'Redis Connection: {self.REDIS_CONNECTION_STR}')
        print(f'Data directory: {self.DATA_DIR}')

        print(f'Contents: {os.listdir(self.DATA_DIR)}')
        try:
            os.mkdir(self.UPLOAD_FOLDER)
            print(f'Created upload dir {self.UPLOAD_FOLDER}')
        except Exception as e:
            if not os.path.exists(self.UPLOAD_FOLDER):
                print('Error creating upload directory!')
                print(e)
                raise e
        try:
            os.mkdir(self.GENERATED_FOLDER)
            print(f'Created generated dir {self.GENERATED_FOLDER}')
        except Exception as e:
            if not os.path.exists(self.GENERATED_FOLDER):
                print('Error creating generated directory!')
                print(e)
                raise e

        print(f'UPLOAD_FOLDER: {self.UPLOAD_FOLDER}')
        print(f'GENERATED_FOLDER: {self.GENERATED_FOLDER}')
