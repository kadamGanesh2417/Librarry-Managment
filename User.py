class user:
    def  __init__(self, name,password,role):
        self.name = name
        self.password = password
        self.role = role
        

    def register(self,uname,password,role):
        print("==="*5+" Registering new User/Admin "+"==="*5)
        with open("users.txt",'a') as file:
            file.writelines(f"{uname} || {password} || {role} "+"\n")
            print("\t\t\t\tRegistered successfully")
            new_user = user(uname,password,role)
            return new_user
            
    
    # def login(self):
    #     uname = input("Enter  UserName: ")
    #     password = input("Enter password: ")
    #     with open("users.txt",'a') as ufile:
    #         data = ufile.readlines()
    #         split_data = data.split(' || ')
    #     if(uname == split_data[0] and password==split_data[1]):
    #         print("\nLogin Successful")
    #         return f"Welcome {uname}"
    #     else:  
    #         print("\nInvalid Credentials")
    #         return False