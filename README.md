This botnet is written with python3 and using socket for communication and I didn't use best practice code just a project.

C2 COMMANDS
sessions              ----->        print all the connected clients.
clear                 ----->        to clear the C2 terminal.
shell <client_id>     ----->        to interact with client by providing the id.
exit                  ----->        to kill all the connected clients and shutdown the C2.
kill <clients_id>     ----->        to kill a specific clients by providing the id.
sendall <command>     ----->        send the command to all connected clients.

CLIENT COMMANDS
quit                  ----->        to kill the client and jump to C2.
back                  ----->        back to c2
cd                    ----->        to change the directory on client.
clear                 ----->        to clear the terminal.

