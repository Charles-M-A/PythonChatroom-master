import csv

import PwdDecrypt
import PwdEncrypt

with open("users.csv", 'r') as csvfile:
    name = input("name:")
    var1 = input("pwd:")
    var0 = PwdEncrypt.encrypt(var1)
    print("1")
flag = 1
with open("usersTest.csv", 'r', newline='') as csvfile:
    print("2")
    read = csv.reader(csvfile)
    count = 0
    for row in read:
        count = count + 1
        print("@@@@", count)
        print("3")
        text = row[0]
        print(text)
        if (name == text):
            print("4")
            flag = 1
            print(var0.decode())
            print(row[1])
            if (PwdDecrypt.decrypt(var0) == PwdDecrypt.decrypt(row[1].encode())):
                print("5")
                print("New connection from:", name)
                # print("Password: ",var0)
                break
            else:
                print("6")
                print("Wrong password!!! Try again.")
                exit(0)
        else:
            flag = 0;
    if flag == 0:
        print("7")
        csvfile.close()
        with open("usersTest.csv", 'a',newline="\n") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            print(var0)
            print(var0.decode().rstrip())
            filewriter.writerow([name, var0.decode()])
            print("New connection from:", name)
            # print("Password: ",var0)
