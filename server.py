
import sys
import socket
import time

#set arguments
dictionary = {}
my_port = sys.argv[1]
parent_ip = sys.argv[2]
parent_port = sys.argv[3]
ips_file = open(sys.argv[4], "r+")

# create socket
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('', eval(my_port)))

# create dictionary data
for line in ips_file:
    new_line = line.rstrip('\n')
    data_from_file = new_line.strip().split(",")
    if(len(data_from_file) < 4):
        dictionary[data_from_file[0]] = [data_from_file[1], data_from_file[2], 0, 'S']
    else:
        remember = eval(data_from_file[3])
        dictionary[data_from_file[0]] = [data_from_file[1], data_from_file[2], remember, data_from_file[4]]
ips_file.close()

# start time
start = time.time()

try:
    # waiting for a massage
    while True:
        data, addr_client = s.recvfrom(1024)
        now = time.time()
        time_passed = now - start
        flag = 0
        # check if server know the ip
        for key in dictionary:
            # if the key is static
            if(data == key.encode() and dictionary[key][3] == 'S'):
                s.sendto(dictionary[key][0].encode(), addr_client)
                s.sendto(dictionary[key][1].encode(), addr_client)
                flag = 1
            else:
                # if the key is dynamic
                if(data == key.encode() and time_passed <= (eval(dictionary[key][1]) - dictionary[key][2])):
                    s.sendto(dictionary[key][0].encode(),addr_client)
                    s.sendto(dictionary[key][1].encode(),addr_client)
                    flag = 1
        # no found ip
        if (flag == 0):
            # request to the parent server
            s.sendto(data, (parent_ip, eval(parent_port)))
            data_ip, addr_server = s.recvfrom(1024)
            data_ttl, addr_server = s.recvfrom(1024)
            # answer to the client
            s.sendto(data_ip, addr_client)
            s.sendto(data_ttl, addr_client)
            # saving recived the data
            dictionary[str(data)[2:-1]] = [str(data_ip)[2:-1], str(eval(data_ttl) + time_passed), 0, 'D']

except KeyboardInterrupt:
    # do nothing
    print()
finally:
    now = time.time()
    time_passed = now - start
    # write a new file
    ips_file = open(sys.argv[4], "w+")
    for key in dictionary:
        if(dictionary[key][3] == 'S'):
            line = key + ',' + dictionary[key][0] + ',' + dictionary[key][1] + ',' + str(dictionary[key][2] + time_passed) + ',S' + '\n'
            ips_file.write(line)
        else:
            if(time_passed <= (eval(dictionary[key][1]) - dictionary[key][2])):
                line = key + ',' + dictionary[key][0] + ',' + dictionary[key][1] + ',' + str(dictionary[key][2] + time_passed) + ',D' + '\n'
                ips_file.write(line)
    # close the file
    ips_file.close()
    # close socket
    s.close()
