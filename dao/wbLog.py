class wbLog(object):
    def __init__(self):
        self.id = None
        self.createTime = None
        self.url = None
        self.cookie = None
        self.commit_url = None
        self.type = None
        self.name = None

    def get_id(self):
        return self.id

    def get_createTime(self):
        return self.createTime

    def get_url(self):
        return self.url

    def get_cookie(self):
        return self.cookie

    def get_commit_url(self):
        return self.commit_url

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def set_id(self, value):
        self.id = value

    def set_createTime(self, value):
        self.createTime = value

    def set_url(self, value):
        self.url = value

    def set_cookie(self, value):
        self.cookie = value

    def set_commit_url(self, value):
        self.commit_url = value

    def set_type(self, value):
        self.type = value

    def set_name(self, value):
        self.name = value

    def get_classinfo(self):
        res = ['id', 'createTime', 'url', 'cookie', 'commit_url', 'type', 'name']
        return res