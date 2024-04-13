import socket
import threading

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("0.0.0.0", 80))
serversocket.listen()
print("Socket WebServer On")


def handle_request(client_socket, address):
    try:
        request_data = client_socket.recv(65535).decode()
        if not request_data:
            return
        
        print()
        print("================================")
        print(f"Connected: {{}}:{{}}".format(address[0], address[1]))

        print(request_data.split("\r\n")[0])

        http_method = request_data.split(' ')[0]
        requested_resource = request_data.split(' ')[1].split("?")[0]
        getdata = {}
        if len(request_data.split(' ')[1].split("?")) == 2 and request_data.split(' ')[1].split("?")[1] != '':
            for datapair in request_data.split(' ')[1].split("?")[1].split("&"):
                [key, value] = datapair.split("=")
                getdata[key] = value
        
        if http_method == 'GET':
            if requested_resource == '/':
                file = open('./templates/index.html', 'r')
                response_body = file.read()
                print('HTTP/1.1 200 OK /')
            elif requested_resource == '/about':
                file = open('./templates/about.html', 'r')
                response_body = file.read()
                print('HTTP/1.1 200 OK /about')
            elif requested_resource == '/postform':
                file = open('./templates/postform.html', 'r')
                response_body = file.read()
                print('HTTP/1.1 200 OK /postform')
            elif requested_resource == '/postresult':
                file = open('./templates/postresult.html', 'r')
                response_body = file.read()
                for key, value in getdata.items():
                    response_body += f"<li>{{}}: {{}}".format(key, value)
                print('HTTP/1.1 200 OK /postresult')
            else:
                file = open('./templates/notfound.html', 'r')
                response_body = file.read()
                print('HTTP/1.1 404 Not Found')
            
            response_headers = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length: {}\n\n'.format(len(response_body)+1024)
            response = response_headers + response_body
        elif http_method == 'POST':
            if requested_resource == '/postform':
                if request_data.find("Content-Length: "):
                    content_length = int(request_data.split("Content-Length: ")[1].split("\r\n")[0])
                    postdata = {}
                    redirect_data = request_data.split("\r\n\r\n")[1][:content_length]
                    for datapair in request_data.split("\r\n\r\n")[1][:content_length].split("&"):
                        [key, value] = datapair.split("=")
                        postdata[key]=value
                    print(f"postdata: {{}}".format(postdata))

                print('HTTP/1.1 200 OK /postform')
                response_headers = f'HTTP/1.1 301 Moved Permanently\nContent-Type: text/html; charset=UTF-8\nLocation: /postresult?{{}}\n\n'.format(redirect_data)
                response = response_headers
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\n\n'
        client_socket.send(response.encode())
        
    except Exception as error:
        print(f"DisConnected with error: {{}}:{{}} {{}}".format(address[0], address[1], error))

    print("================================")
    print()
    client_socket.close()

try:
    while True:
        (clientsocket, address) = serversocket.accept()
        t = threading.Thread(target=handle_request, args=(clientsocket, address))
        t.daemon = True
        t.start()
except Exception as error:
    print(f"error occured: {{}}".format(error))
finally:
    serversocket.close()