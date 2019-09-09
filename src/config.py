import os


class Config(object):
    UPLOAD_FOLDER = '/tmp/emojigen/uploaded'
    GENERATED_FOLDER = '/tmp/emojigen/generated'
    REDIS_HOST = 'redis://192.168.1.120:6379'

    def __init__(self):
        try:
            os.mkdir(self.UPLOAD_FOLDER)
        except:
            pass
        try:
            os.mkdir(self.GENERATED_FOLDER)
        except:
            pass


class WindowsConfig(Config):
    UPLOAD_FOLDER = r'C:\dev\emojigen\uploaded'
    GENERATED_FOLDER = r'C:\dev\emojigen\generated'

    def __init__(self):
        super().__init__()
