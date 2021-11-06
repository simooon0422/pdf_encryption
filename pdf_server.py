import socket
import threading
import PyPDF2
import base64
import os
from time import sleep


# Connection Data
host = '127.0.0.1'
port = 8081

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients And Received PDFs
clients = []
received_pdfs = []


# Sending Messages To All Connected Clients
def broadcast(client):
    while True:
        try:
            while received_pdfs[clients.index(client)]:
                print(f'Number of messages: {len(received_pdfs)}')
                base_pdf = received_pdfs[clients.index(client)].pop(0)
                decode_pdf(base_pdf, client)
                encrypt_pdf(f'server_temp/decoded_pdf_{clients.index(client)}.pdf', client)
                encoded_encrypted_pdf = encode_pdf(f'server_temp/encrypted_file_{clients.index(client)}.pdf')
                client.send(encoded_encrypted_pdf)
        except:
            break
        sleep(0.1)


# Handling Messages From Clients
def handle(client):
    clients.append(client)
    received_pdfs.append(list())

    while True:
        try:
            # Broadcasting Messages
            received_pdf = client.recv(2048)
            print(received_pdf)
            received_pdfs[clients.index(client)].append(received_pdf)
            print(received_pdfs)
            sleep(1)
        except:
            # Removing And Closing Clients, Clearing List of Received PDFs
            del received_pdfs[clients.index(client)]
            clients.remove(client)
            client.close()
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f'Connected with {(str(address))}')

        # Start Handling And Broadcast Threads For Client
        threading.Thread(target=handle, args=(client,)).start()
        threading.Thread(target=broadcast, args=(client,)).start()


def encrypt_pdf(pdf_file, client):
    file = open(pdf_file, 'rb')
    # Create reader and writer object
    pdf_reader = PyPDF2.PdfFileReader(file)
    pdf_writer = PyPDF2.PdfFileWriter()

    # Add all pages to writer
    for page_num in range(pdf_reader.numPages):
        pdf_writer.addPage(pdf_reader.getPage(page_num))

    # Encrypt with your password
    pdf_writer.encrypt('mypassword')

    # Write it to an output file. (you can delete unencrypted version now)
    with open(f'server_temp/encrypted_file_{clients.index(client)}.pdf', 'wb') as result_pdf:
        pdf_writer.write(result_pdf)

    file.close()
    os.remove(pdf_file)


def encode_pdf(pdf_file):
    pdf_to_encode = open(pdf_file, 'rb')
    encoded_pdf_file = base64.b64encode(pdf_to_encode.read())
    pdf_to_encode.close()
    os.remove(pdf_file)
    return encoded_pdf_file


def decode_pdf(pdf_file, client):
    with open(f'server_temp/decoded_pdf_{clients.index(client)}.pdf', 'wb') as file_to_save:
        decoded_pdf_file = base64.b64decode(pdf_file)
        file_to_save.write(decoded_pdf_file)


print('Server is listening ...')
receive()
