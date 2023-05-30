class feelCheck(object):
    def __init__(self):
        self.id = None
        self.createTime = None
        self.action_name = None
        self.pos = None
        self.neg = None
        self.ord = None
        self.state = None
        self.updateTime = None

    def get_id(self):
        return self.id

    def get_createTime(self):
        return self.createTime

    def get_action_name(self):
        return self.action_name

    def get_pos(self):
        return self.pos

    def get_neg(self):
        return self.neg

    def get_ord(self):
        return self.ord

    def get_state(self):
        return self.state

    def get_updateTime(self):
        return self.updateTime

    def set_id(self, value):
        self.id = value

    def set_createTime(self, value):
        self.createTime = value

    def set_action_name(self, value):
        self.action_name = value

    def set_pos(self, value):
        self.pos = value

    def set_neg(self, value):
        self.neg = value

    def set_ord(self, value):
        self.ord = value

    def set_state(self, value):
        self.state = value

    def set_updateTime(self, value):
        self.updateTime = value

    def get_classinfo(self):
        res = ['id', 'createTime', 'action_name', 'pos', 'neg', 'ord', 'state', 'updateTime']
        return res