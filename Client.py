from socket import*
import time
import sys


#print the option for client to select
def printServerOption():
    print("-------------------------------------------------------")
    print("                        Menu                           ")
    print("-------------------------------------------------------")
    print("(1) Get server name and IP")
    print("(2) Get statistics (mean, minimum, maximum)")
    print("(3) Quit program")
    print("Enter you choice (1, 2 or 3): ")
    return input()

def main():
    #Initialise client's socket
    serverName = "localhost"
    serverPort = 5000 #initialise server socket which is 5000
    clientSocket = socket(AF_INET, SOCK_STREAM) #initialise it as ipv4 and tcp port 
    clientSocket.connect((serverName, serverPort))
    #Initialise the message
    messageToSend = ""
    messageReceived = ""
    loginAttempt = 0 #Set the login attempt to 0
    #keep running unless client input 3 which is to exit
    while loginAttempt < 3:
        username = input("Please enter Username: ").lower() # get the username and set it lowercase
        password = input("Please enter Password: ")
        userDetails ="authentication"+ username +" "+ password #set the format as "autenticationanyname anypassword
        clientSocket.send(userDetails.encode("utf-8"))
        validation = clientSocket.recv(1024).decode("utf-8")
        if validation == "Yes":
            break #if the return resut is yes, it will break the loop and display user the menu to select
        else:
            print("Incorrect username or password, please try again")
            loginAttempt += 1 #to increase the login attempt, once it reach 3, it will break the loop
    if loginAttempt == 3:
        print("You have been disconnected, beucase maximum you have pass maximum login attempt")
        time.sleep(5)#before closing the application, give client 5 second to read the message
        sys.exit()
    while messageToSend != "3":
        #if the message recieve is input, which is a special case than it will prompt client to enter the organisation name and send it to server agian, before reprinting the option for client to select
        if messageReceived == "input":
            serverName = input("Please enter server name: ")
            serverName = "0" + serverName #send server 0 following with the request organisation name, thus server will know which operation to perform
            clientSocket.send(serverName.encode("utf-8")) #encode the message and send
            messageReceived = clientSocket.recv(1024).decode("utf-8") #decode the message recieved from server
            print(messageReceived)#print the message
        messageToSend = printServerOption() #print the option and get the option client selected
        clientSocket.send(messageToSend.encode("utf-8")) # encode the message and send
        messageReceived = clientSocket.recv(1024).decode("utf-8") #decode the message before print it
        print(messageReceived)
main()
    
                      

