#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the MsgHdr and MsgCtl class.
"""

class MsgHdr(object):
    HEADERLEN = 9
    KEYWORDCLIENT = [
    "PLY_LOG_C",  #Inform server new player's name, with name and password
    "REG_USR_C",  #Inform server to register a new user
    "FRS_CRM_C",  #Inquire server for chess room information
    "CHT_MSG_C",  #Send chat message to server
    "JON_POS_C",  #Select a seat
    "LEV_POS_C",  #Deselect a seat
    "SND_LAY_C",  #Send layout to server
    "SND_MOV_C",  #Send a movement by user
    "ASK_MOV_C",  #Query a movement
    "ASK_STP_C",  #Query total step number
    "GAM_YLD_C",  #Yield
    "GAM_QUT_C",  #Quit game / Disconnect server
    "ASK_CHS_C",  #Query a chess value
    "SAV_LAY_C",  #Ask server to save game layout
    "GET_RCD_C",  #Ask server to transfer game record
    "PLY_DAT_C",  #Query player data
    ]

    KEYWORDSERVER = [
    "PLY_NAM_S",  #Tell all clients player's name
    "GAM_RST_S",  #Tell all clients to reinitialize
    "CHT_MSG_S",  #Broadcast chat message to clients
    "JON_POS_S",  #Client joined specified seat
    "LEV_POS_S",  #Client left specified seat
    "AT__POS_S",  #Player is at specified seat
    "SND_LAY_S",  #Ask client to send layout
    "SND_MOV_S",  #Tell client the specified move
    "ASK_MOV_S",  #Ask client to send movement, or to wait
    "STP_NUM_S",  #Return step number
    "GAM_DIE_S",  #Tell all clients player is died
    "GAM_OVR_S",  #Return game result to client
    "CHS_VAL_S",  #Return chess value
    "RCD_STR_S",  #Return game record in string
    "LOG_RES_S",  #Return log result
    "REG_RES_S",  #Return register result
    "PLY_DAT_S",  #Return player data
    ]

class MsgCtl(object):
    """
        This is a redesign of JAVA version messages.
    """
    MESSAGESEP = "||"
    ARGSEP = ","
    #Message to receive
    MSGRCV = []
    #Message to send
    MSGSND = []

    def split(self, longMessage):
        return longMessage.split(MsgCtl.MESSAGESEP)

    def join(self, shortMessages):
        return MsgCtl.MESSAGESEP.join(shortMessages)

    def parseBody(self, format, message):
        ret = []
        for ch in format:
            if not message: # error occurred
                return
            if message.find(MsgCtl.ARGSEP) != -1:
                s, message = message.split(MsgCtl.ARGSEP,1)
            else:
                s, message = message, ''
            #print "s = ",s,"message = ",message
            if ch == 's':
                try:
                    larg = int(s.strip())
                    s, message = message[:larg], message[larg+len(MsgCtl.ARGSEP):]
                    ret.append(s)
                except ValueError:
                    print("Warning: invalid integer syntax : '%s'" %(s))
                    return
            elif ch == 'i':
                try:
                    num = int(s.strip())
                    ret.append(num)
                except ValueError:
                    print("Warning: invalid integer syntax : '%s'" %(s))
                    return

        if message != '':
            return
        return tuple(ret)

    def parse(self, message):
        #return None for errors. need subclassing
        pass

    def createBody(self, format, args):
        if not format:
            return
        if len(args) != len(format):
            return
        ret = []
        args = list(args)
        args.reverse()
        for ch in format:
            if ch == "i":
                ret.append(str(args.pop()))
            elif ch == "s":
                arg = str(args.pop())
                larg = str(len(arg))
                ret.append(larg)
                ret.append(arg)
            else:
                return
        return MsgCtl.ARGSEP.join(ret)

    def create(self, hdr, args):
        #return None for errors, need subclassing
        pass

class ClientMsgCtl(MsgCtl):
    MSGRCV = MsgHdr.KEYWORDSERVER
    MSGSND = MsgHdr.KEYWORDCLIENT
    def parse(self, message):
        hdr, msg = message[:MsgHdr.HEADERLEN], message[MsgHdr.HEADERLEN + len(MsgCtl.ARGSEP):]
        args = ()
        if not hdr in MSGRCV:
            return
        if hdr in ["PLY_DAT_S"]:
            args = self.parseBody("ss", msg)
            if not args:
                return
        elif hdr in ["GAM_RST_S", "SND_LAY_S"]:
            if msg.strip():
                return
        elif hdr in ["PLY_NAM_S", "SND_MOV_S", "RCD_STR_S"]:
            args = self.parseBody("s", msg)
            if not args:
                return
        elif hdr in ["CHT_MSG_S", "JON_POS_S", "LEV_POS_S", "AT__POS_S", "CHS_VAL_S"]:
            args = self.parseBody("is", msg)
            if not args:
                return
        elif hdr in ["ASK_MOV_S", "STP_NUM_S", "GAM_DIE_S", "GAM_OVR_S", "LOG_RES_S", "REG_RES_S"]:
            args = self.parseBody("i", msg)
            if not args:
                return
        return (hdr, args)

    def create(self, hdr, args):
        if not hdr in MSGSND:
            return
        if hdr in ["PLY_LOG_C", "REG_USR_C"]:
            body = self.createBody("ss", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        elif hdr in ["FRS_CRM_C", "ASK_STP_C", "GAM_YLD_C", "GAM_QUT_C", "SAV_LAY_C", "GET_RCD_C"]:
            if len(args) != 0:
                return
            return hdr
        elif hdr in ["CHT_MSG_C", "SND_LAY_C", "SND_MOV_C"]:
            body = self.createBody("s", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        elif hdr in ["JON_POS_C", "LEV_POS_C", "ASK_MOV_C", "ASK_CHS_C", "PLY_DAT_C"]:
            body = self.createBody("i", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        return

class ServerMsgCtl(MsgCtl):
    MSGRCV = MsgHdr.KEYWORDCLIENT
    MSGSND = MsgHdr.KEYWORDSERVER
    def parse(self, message):
        hdr, msg = message[:MsgHdr.HEADERLEN], message[MsgHdr.HEADERLEN + len(MsgCtl.ARGSEP):]
        args = ()
        if not hdr in MSGRCV:
            return
        if hdr in ["PLY_LOG_C", "REG_USR_C"]:
            args = self.parseBody("ss", msg)
            if not args:
                return
        elif hdr in ["FRS_CRM_C", "ASK_STP_C", "GAM_YLD_C", "GAM_QUT_C", "SAV_LAY_C", "GET_RCD_C"]:
            if msg.strip() != 0:
                return
        elif hdr in ["CHT_MSG_C", "SND_LAY_C", "SND_MOV_C"]:
            args = self.createBody("s", msg)
            if not args:
                return
        elif hdr in ["JON_POS_C", "LEV_POS_C", "ASK_MOV_C", "ASK_CHS_C", "PLY_DAT_C"]:
            args = self.createBody("i", msg)
            if not args:
                return
        return (hdr, args)

    def create(self, hdr, args):
        if not hdr in MSGSND:
            return
        if hdr in ["PLY_DAT_S"]:
            body = self.createBody("ss", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        elif hdr in ["GAM_RST_S", "SND_LAY_S"]:
            if len(args) != 0:
                return
            return hdr
        elif hdr in ["PLY_NAM_S", "SND_MOV_S", "RCD_STR_S"]:
            body = self.createBody("s", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        elif hdr in ["CHT_MSG_S", "JON_POS_S", "LEV_POS_S", "AT__POS_S", "CHS_VAL_S"]:
            body = self.createBody("is", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        elif hdr in ["ASK_MOV_S", "STP_NUM_S", "GAM_DIE_S", "GAM_OVR_S", "LOG_RES_S", "REG_RES_S"]:
            body = self.createBody("i", args)
            if body:
                return hdr + MsgCtl.ARGSEP + body
        return

if __name__=='__main__':
    a = MsgCtl()
    b = a.parseBody('sis','4,abcd,5,5,abcde')
    print b
    c = a.createBody('sis',b)
    print c
