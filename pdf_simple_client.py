import socket
import threading
import base64
import PyPDF2
import os


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8081))


# Listening to Server and Sending Nickname
def receive_encrypted_pdf():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(2048)
            decode_pdf(message)

        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def send_pdf(pdf_file):
    pdf_file = open(pdf_file, 'rb')
    encoded_pdf_file = base64.b64encode(pdf_file.read())
    # print(encoded_pdf_file)
    client.send(encoded_pdf_file)


def encode_pdf(pdf_file):
    pdf_to_encode = open(pdf_file, 'rb')
    encoded_pdf_file = base64.b64encode(pdf_to_encode.read())
    pdf_to_encode.close()
    return encoded_pdf_file


def decode_pdf(pdf_file):
    with open('decoded_pdf.pdf', 'wb') as file_to_save:
        decoded_pdf_file = base64.b64decode(pdf_file)
        file_to_save.write(decoded_pdf_file)


def encrypt_pdf(pdf_file):
    file = open(pdf_file, 'rb')
    # Create reader and writer object
    pdf_reader = PyPDF2.PdfFileReader(file)
    pdf_writer = PyPDF2.PdfFileWriter()

    # Add all pages to writer
    for page_num in range(pdf_reader.numPages):
        pdf_writer.addPage(pdf_reader.getPage(page_num))

    # Encrypt with your password
    pdf_writer.encrypt('password')

    # Write it to an output file. (you can delete unencrypted version now)
    with open(f'encrypted_{pdf_file}', 'wb') as result_pdf:
        pdf_writer.write(result_pdf)

    file.close()
    os.remove(pdf_file)


send_pdf('pdf_1.pdf')
receive_encrypted_pdf()


# test_pdf = encode_pdf('pdf_1.pdf')
# decode_pdf(test_pdf)
# encrypt_pdf('decoded_pdf.pdf')
