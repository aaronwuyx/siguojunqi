class Message:
    def __init__(self,message = '',fromURL=None,fromPort=None):
        self.message = message
        self.cmd,arg = message.split(' ',1)
        self.arg = arg.split()
        self.creator = (fromURL,fromPort)
    def send(self,toURL,toPort):
        return
    def receive(self):
        return self
