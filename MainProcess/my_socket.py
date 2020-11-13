from baseModule.SocketMoudule import baseSocket

class mySocket(baseSocket):
    def __init__(self,main,h,p):
        self.host = h
        self.port = p
        baseSocket.__init__(self,self.host,self.port)
        self.main = main
    def Send_Recv(self,command):
        buffer = '_________'
        buffer = command + buffer
        mode = super().Send_Recv(buffer[0:10])
        mode = mode[0:9]
        mode = mode.replace('_','')
        SList = mode.split('|')
        return SList

    def loopSocket(self):
        while True:
            try:   
                while True:
                    if not self.main.systemState:
                        print("endSocket")
                        return
                    recvBuffer=self.Send_Recv('0')
                    if recvBuffer[0] == '1':
                        self.main.control.CamCheckBus(recvBuffer[1])
                    else :
                        print("통신에러")
            except:
                baseSocket.__init__(self,self.host,self.port)
            




if __name__ == "__main__":
    print("start")
    st= mySocket(None,"127.0.0.1",12345)
    st.loopSocket()



