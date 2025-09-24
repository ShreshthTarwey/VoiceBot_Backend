import smtplib
email = input("Sender Email: ")
reciver_email = input("Reciever Email: ")


subject = input("SUBJECT: ")
message = input("MESSAGE: ");

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com",587)

server.starttls()

server.login(email,"chrj nbut lzfd hdex")

server.sendmail(email,reciver_email,text)

print("Done!!")