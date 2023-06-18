import SocketServer
import os

vessels = ["Ship", "Relay", "Probe"]


vesselDirectory = "/KSP/LMPServer/Universe/Vessels"

def getSub(string, name):
    i = [s.split()[0] for s in string.split("\n")]
    print(i.index(name))
    temp = "\n".join(string.split("\n")[i.index(name)+2:])
    opened = 1
    for i in range(len(temp)):
        if temp[i]=="{":
            opened+=1
        if temp[i]=="}" and opened==1:
            temp = temp[:i]
            break
    print(temp)
    
    return 
def getField(string, name):
    i = [s.split()[0] for s in string.split("\n")]
    print(i.index(name))
    temp = string.split("\n")[i.index(name)].split(" = ")[-1]
    print(temp)
    return temp

def countVessels():
    count = 0
# Iterate directory
    for path in os.listdir(vesselDirectory):
        # check if current path is a file
        if os.path.isfile(os.path.join(vesselDirectory, path)):
            count += 1
    return count
    
def getVessel(id):
    path = os.listdir(vesselDirectory)[id]
    l = open(os.path.join(vesselDirectory, path)).read()
    getSub(l, "ORBIT")
    getField(l, "name")
    return getField(l, "name")


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def parseCommand(self):
        if self.data == "vesselsCount":
            return countVessels()
        if self.data.split()[0] == "vessel":
            
            return getVessel(int(self.data.split()[1]))
            

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if self.client_address[0]=="127.0.0.1":
            print "{} wrote:".format(self.client_address[0])
            print self.data
            self.request.sendall(str(self.parseCommand()))
        # just send back the same data, but upper-cased
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 11242
    
    for path in os.listdir(vesselDirectory):
        l = open(os.path.join(vesselDirectory, path)).read()
        getSub(l, "ORBIT")
        getField(l, "name")
        break

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except BaseException as e:
        server.stop()