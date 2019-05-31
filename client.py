import socket
import select
import sys
#create client socket
s=socket.socket()
#defining the server's port and ip to which we want to connects
ip='127.0.0.1'#this ip is for self request
port=3332
#connect to the server
s.connect((ip,port))
#global variable to keep others locked whenever other player presses buzzer
LOCK=False
while True:
    ques=s.recv(1024)
    if ques=='END':
        break
    print "Question is :\n",ques
    print "press ENTER to hit BUZZER!"
    global LOCK
    LOCK=False
    list_inputs=[sys.stdin,s]
    while True:
        flag=0
        x=select.select(list_inputs,[],[])[0]
        for i in x:
            if i==s:
                mess=i.recv(1024)
                if int(mess)==1:
                    print "Your chance, Give your ANSWER"
                    ans=sys.stdin.readline()
                    i.send(ans)
                    flag=1
                elif int(mess)==0:
                    print "Other PLayer pressed the BUZZER\n"
                    s.send('0')
                    LOCK=True
                    flag=1
            if i==sys.stdin and LOCK==False:
                sys.stdin.readline()
                s.send("1")
        if flag==1:
            break
print "Contest Ended"
print s.recv(1024)
print s.recv(1024)
s.close()

