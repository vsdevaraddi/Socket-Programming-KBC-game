import socket
#to generate random number
import random
#for multi threading
import threading
#structure to a user

#creating server sockets
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
#for multi threading
from threading import Thread

#socket ip and port number
ip=''
port=3332

#binding the ip and port to socket
#deciding max queue in connecting to each socket s.listen
try:
    server_socket.bind((ip,port))
except socket.error as err1:
    print("error in socket "+str(err1))
server_socket.listen(5)

#reading questions and answers from a file
f=open("question_list.txt","r")
listof_ques=f.readlines()
f1=open("answer_list.txt","r")
listof_ans=f1.readlines()
#length of the this list is mentained in this variable
length_list=len(listof_ques)
f.close()
f1.close()

#accepting connections from 3 clients on server_socket socket

c1, c1_addr=server_socket.accept()
print "Accepted connection from ",c1_addr
client1=[c1,c1_addr,0]
c2, c2_addr=server_socket.accept()
print "Accepted connection from ",c2_addr
client2=[c2,c2_addr,1]
c3, c3_addr=server_socket.accept()
print "Accepted connection from ",c3_addr
client3=[c3,c3_addr,2]
del c1,c1_addr,c2,c2_addr,c3,c3_addr
clients=[client1,client2,client3]
scores=[0,0,0]
def message_sender(client,message,clients):
    client[0].send(message)


def multithread(clients,fun,message):
    threads=[]
    for i in clients:
        t=Thread(target=fun,args=(i,message,clients,))
        threads.append(t)
    return threads


def multirecv(client,answer,clients):
    x=client[0].recv(1)
    if int(x)==1:
        for i in clients:
            if i!=client:
                i[0].send("0")
        client[0].send("1")
        ans=client[0].recv(1024)
        if ans==answer:
            print "answer is correct"
            scores[client[2]]=scores[client[2]]+1


while(scores[0]!=5 and scores[1]!=5 and scores[2]!=5):
    print "going to next question"
    x=random.randint(0,length_list)
    length_list=length_list-1
    question=listof_ques.pop(x)
    ans=listof_ans.pop(x)
    #sending question to all
    threads=multithread(clients,message_sender,question)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    del threads
    threads=multithread(clients,multirecv,ans)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    del threads
#end game and notify all clients
for i in clients:
    i[0].send('END')
    i[0].send("Scores are "+str(scores[0])+", "+str(scores[1])+", "+str(scores[2])+". Your Score is "+str(scores[i[2]]))
    if scores[i[2]]==5:
        i[0].send(" Congratulations and you are the WINNER")
    else:
        i[0].send(".")
print "Contest Ended\n"


server_socket.close()
    

