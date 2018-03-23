from socket import *
from threading import *
import statistics

#read the file and store it into serverData list
def readFile(serverData):
    try: 
        file = open('organisations.txt', 'r')
        #loop through each line in file
        for line in file:
            serverData.append(line.strip('\n\t').split()) #strip out any newline or tab and split the element
        return serverData
    except IOError: #if the file doesn't exist, it prompt the administrator that file doesn't exist.
        print("The file doesn't exist")
        print('organisations.txt')

def readUserFile(userData):
    try: 
        file = open('users.txt', 'r')
        #loop through each line in file
        for line in file:
            userData.append(line.strip('\n\t').split()) #strip out any newline or tab and split the element
        return userData
    except IOError: #if the file doesn't exist, it prompt the administrator that file doesn't exist.
        print("The file doesn't exist")
        print('users.txt')

def userAuthentication(userDetails, userData):
    userData = readUserFile(userData) #read the user data from users.txt
    for x in range(0,len(userData)): #loop from 0 to last
        if userDetails[0] == userData[x][0]: #if the username matchs to the list's username
            if userDetails[1] == userData[x][1]: #if the password matches to the list's passord
                return "Yes" #if both condition are meet, return yes and break the authentication process
                break
    return "No" #if both condition are not meet after looping all the list, it will return No indicating it didn't success authenticate the user file
        

#calculatethe mean, max and min and return the value 
def getStatistics(serverData):
    serverData = readFile(serverData) #read the organisation data from organisation.txt
    connection = []
    #loop through each element
    for line in serverData:
        connection.append(int(line[-1])) #appead only last element of line into connection
    mean = statistics.mean(connection) #calculate mean
    maximum =  max(connection) #calculate max
    minimum = min(connection) #calculate min
    return (mean, maximum, minimum) #return all 3 calculation

#compare client's inputed name with the server data and return the website and ip address
def getOrganisation(name, serverData):
    serverData = readFile(serverData)
    organisationInfo = []
    #loop through each element
    for line in serverData:
        organisationInfo.append(line[0:3])#append only 1st 3 element of line into organisationInfo
    #loop through whole orgranisationInfo
    for x in range(0, len(organisationInfo)):
        #if the name matches to the organisation's name than return the domain name and ip address
        if name.lower() == organisationInfo[x][0].lower():
            return (organisationInfo[x][1] , organisationInfo[x][2])
            break
    #else return error message
    else:
        message = "Sorry, mentioned organisation's server is not found, please try again with different organisation"
        return ("Error", message) #counter to indicate no server is found
        
    

#Class for the client Thread
class clientHandler(Thread):
    #Initialize the thread
    def __init__(self, client, address):
        Thread.__init__(self)
        self._client = client
        self._address = address

    def run(self):
        try:
            #Initialize
            while True:
                serverData = []
                clientData = []
                messageReceived = "" #reset the messageRecevied 
                messageReceived = self._client.recv(1024).decode("utf-8")

                #To perform user authentication process once it recieve message from client starting with "authenticationanyname anypassword
                if messageReceived[0:13] =="authentication": #to select the 1st 12 letter which is "authentication"
                    print("test")
                    userDetails = messageReceived[13:].split() #split the username and password into ['anyname','anypassword']
                    messageToSend = userAuthentication(userDetails, clientData) #pass the user login details and client data list
                    self._client.send(messageToSend.encode("utf-8"))
                    
                #Reply client with information about the organisation's server name and ip
                elif messageReceived[0] == "0":
                    domainName, IP = getOrganisation(messageReceived[1:], serverData)
                    #Message format is ("Error", message), thus IP contain the message
                    #if the domainName is error, send client the error message about organisation information not found
                    if domainName == "Error":
                        messageToSend = IP
                    #else send client the organisation information
                    else:
                        messageToSend = messageReceived[1:] + "'s domain name is %s" %domainName + \
                                        " and the IP address is %s" %IP
                    self._client.send(messageToSend.encode("utf-8"))

                #Prompts user to enter an organisation name 
                elif messageReceived == "1":
                    self._client.send("input".encode("utf-8"))    
                                    
                #Get statistics(mean, minimum, maximum)
                elif messageReceived == "2" :
                    mean, maximum, minimum = getStatistics(serverData)
                    messageToSend = "The mean connection for all the server is %d" %mean + '\n' \
                                    "The maximum connection among the server is %d" %maximum +'\n' \
                                    "The minimum connection among the server is %d" %minimum 
                    self._client.send(messageToSend.encode("utf-8"))
                #if the option is 3, server will close the connection for client
                elif messageReceived == "3":
                    self._client.close()
                    print("Client" , self._address,"has disconnected")
                    break
                #if the option is neither 1, 2, or 3 than return invalid option selected
                else:
                    self._client.send("The selected option is invalid".encode("utf-8"))
        except:
            print("Client", self._address, "suddenly disconnected")

def main():
    #Initialize the server socket
    serverName = "localhost"
    serverPort = 5000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, serverPort))
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.listen(10)
    print("Server is waiting for connection...")
    #to make sure server is forever online
    while True:
        client, address = serverSocket.accept() #accept client's socket
        print("Client has connected from: ", address)
        handler = clientHandler(client, address) #create an client handler object with client's information and address
        handler.start() #start the threat to handle the client


main()
