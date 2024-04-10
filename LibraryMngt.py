from Book import Book
import getpass 
from User import *
from BookMngt import LibraryMngt
from random import randint as rd
import os
import time
from customExceptions import *

if __name__ == "__main__":
    obj = LibraryMngt()
    # print('==='*18 + ' LIBRARY MANAGEMENT SYSTEM ' + '==='*18+"\n")
    # Login Process
    inp = 0
    while inp!=3:
        print('==='*18 + ' LIBRARY MANAGEMENT SYSTEM ' + '==='*18+"\n")
        print(""" 
                \t\t\t\t\t-----------------------  
                \t\t\t\t\t 1. Register User (Only user role)
                \t\t\t\t\t 2. Login
                \t\t\t\t\t 3. Exit
                \t\t\t\t\t-----------------------
    """)
        inp = int(input("Enter Choice: "))
        if inp==1:
            role = "User"
            LibraryMngt.register(role)
        elif inp==2:
            print("\t\t\t\t"+"-----" * 3 + " Login " + "-----" * 3)
            username = input(f"\t\t\t\t\033[1m User Name: \033[0m")
            password = getpass.getpass(f"\t\t\t\t\033[1m Password: \033[0m")
            print("\t\t\t\t"+"-----" * 3 + " Submit " + "-----" * 3)

            #validate over users file and based on role
            with open("users.txt",'r') as ufile:
                userdata = ufile.readlines()
                try: 
                    if not userdata:
                        raise Empty_file_Error
                except Empty_file_Error as e:
                    print(e)
                for data in userdata:
                    if data.endswith("\n"):
                        data = data.replace('\n','')
                    else:
                        data = data
                    split_data = data.split(" || ")
                    if(username == split_data[0] and password==split_data[1] and split_data[2]=="Admin"):
                            print("\n Admin Login successful \n")
                            ch = 0
                            while ch!=5 or ch!='L':

                                print('==='*18 + ' LIBRARY MANAGEMENT SYSTEM (Admin Module)' + '==='*18)
                                print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t ----------------------------')
                                print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1m  Welcome Admin : {username} \033[0m' + " press(L) -> Logout")
                                print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t ----------------------------\n')
                                
                                print('''\t\t\t\t
                                                        \033[1m------ Menu ------
                                --------------------------------    --------------------------------
                                    1. Add Book                          5. Add Admin
                                --------------------------------    --------------------------------
                                    2. Display Books                     6. Delete Book
                                --------------------------------    --------------------------------
                                    3. Get Borrow Book Report            7. Remove Admin
                                --------------------------------    --------------------------------
                                    4. Get Available Book Report         8. Update Book
                                --------------------------------    --------------------------------\033[0m

                                ''')
                                ch = input("Choice : ")
                            
                                print("\n")
                                if ch == '1':
                                    print("\t\t\t\t"+"-----"*5+" Add book Section "+"------"*5 + "\n")
                                    bid = input("\t\t\t\tBid : ")
                                    Baname = input("\t\t\t\tBook Name: ")
                                    Author = input("\t\t\t\tAuthor: ")
                                    Noc = int(input("\t\t\t\tAvailable Copies: "))
                                    Status = "Available"
                                    #check if Bid is already exist
                                    with open('Books.txt','r') as fp:
                                        for book in fp:
                                            data = book.split("|")
                                            if data[0]==bid or data[1]==Baname:
                                                print("\t\t Book Id or Book already Exist \n ")
                                                break
                                        else:
                                            e = Book(bid,Baname,Author,Status,Noc)
                                            obj.Add_Book(e)

                                elif ch == '2':
                                    
                                    LibraryMngt.Display_books(1)

                                elif ch == '3':
                                    try:
                                        LibraryMngt.Get_Borrowed_Book()
                                    except Empty_file_Error as e:
                                        print(e)
                                    print("\n")
                            
                                elif ch == "4":
                                    LibraryMngt.Get_Available_Books(1)
                                    print("\n")

                                elif ch=='5':
                                    role = "Admin"
                                    opt = rd(1,999)
                                    try: 
                                        with open('OTP.txt', 'a')as f:
                                            f.write(str(opt))
                                            print("\nYour OTP is sent to the OTP FILE: ")
                                        print("file created")
                                        
                                        opt_chance = 3
                                        stored_otps = open('OTP.txt').read()
                                        print("OPT: ",stored_otps)

                                        while opt_chance>0:
                                            u_opt = str(input("Enter OTP from otp file: "))
                                            if u_opt==stored_otps:
                                                print("OTP Verified")
                                                LibraryMngt.register(role)
                                                os.remove('OTP.txt')
                                                break
                                            else:
                                                print(f"\nInvalid OTP \nPlease try again.\nAttempts left: {opt_chance}")
                                                opt_chance-=1
                                        else:
                                            print("\nMaximum attempts exceeded.")
                                            os.remove('OTP.txt') 
                                    
                                        
                                    except Exception as E:
                                        print(f"Error Occurred: {E}")

                                elif ch=='6':
                                    LibraryMngt.Display_books(1)
                                    book_id = input("Select Book to delete: ")
                                    LibraryMngt.delete_book(book_id)

                                elif ch == "7":
                                    Admin = input("Admin name: ")
                                    LibraryMngt.Remove_Admin(Admin,username)

                                elif ch=="8": 
                                    LibraryMngt.Display_books(1)
                                    bname = input("Book Name: ")
                                    LibraryMngt.update_book(bname)

                                elif ch == "L" or ch=="l":
                                    print("-----"*5 + " Exiting from Admin Module "+ "-----"*5)
                                    time.sleep(2)
                                    print("-----"*5+ " Thanks for the using the System "+"-----"*5)
                                    break
                                
                            else:
                                print("Wrong Choice Entered")

                    elif(username == split_data[0] and password==split_data[1] and split_data[2]=="User"):
                        print("\n User Login successful \n")
                        ch = 0
                        while ch!=5:
                            print('==='*18 + ' LIBRARY MANAGEMENT SYSTEM (User Module)' + '==='*18)
                            print('\t\t\t\t\t\t\t\t\t\t\t\t ----------------------------')
                            print(f'\t\t\t\t\t\t\t\t\t\t\t\t  \033[1m Welcome User : {username} \033[0m')
                            print('\t\t\t\t\t\t\t\t\t\t\t\t ----------------------------')
                            print('''\t\t\t\t\t 
                                \033[1m ------ Menu ------
                            
                            --------------------------------   
                                1. Display Books
                            --------------------------------
                                2. Borrow Book 
                            --------------------------------
                                3. Return Book
                            --------------------------------
                                4. Search Book
                            --------------------------------
                                5. Exit
                            --------------------------------\033[0m

                            ''')
                            try:
                                
                                ch  = int(input("\t\tChoice:  "))

                                if ch == 1:
                                    LibraryMngt.Display_books(1)
                                    print("\n")

                                elif ch == 2:
                                    LibraryMngt.Get_Available_Books(1)
                                    bid = int(input("\t\t Book ID  to be borrowed:  "))
                                    LibraryMngt.borrow_book(str(bid),username)

                                elif ch == 3:
                                    print("===" * 5 + " Return book Section " + "===" * 5 + "\n")
                                    has_data = False
                                    try: 
                                        with open("Borrowed_Register.txt", 'r+') as register_data:
                                            register_lines = register_data.readlines()
                                            if not register_lines:
                                                raise Empty_file_Error
                                            else:
                                                for data in (register_lines):
                                                    split_data = data.split(" || ")
                                                    if split_data[3] in username and split_data[5]=="Borrowed":
                                                        print(f"Issue_number: {split_data[0]} | Book Id: {split_data[1]} | Book Name: {split_data[2]}")
                                                        has_data = True
                                                    else:
                                                        pass
                                                if has_data:

                                                    Issue_ID = int(input("\t\t Enter Issue ID to return Book: "))
                                                    LibraryMngt.Return_book(str(Issue_ID),username)
                                                else:
                                                    print(f"{username} Does not issued any book !")

                                    except Empty_file_Error as E:
                                        print(E)
                                                                        
                                elif ch ==4:     
                                    LibraryMngt.Search_Book()

                                elif ch ==5:
                                    time.sleep(2)
                                    print("-----"*5 + " Exited from User Module " + "----"*5)
                                    break
                                    
                            except ValueError as E:
                                print("\t\tEnter Only numbers ||")            
                        else:
                            print("Wrong Choice..") 
                    
                    elif (username == split_data[0] and password!=split_data[1]):
                        print("\t\t\t\nInvalid Credentials")
                    else:
                        pass    
            # If the user is new then create a new account
        
        elif inp==3:
            print("-----"*5 + " Exiting from  the Application " + "----"*5)
            time.sleep(2)
            print("-----"*5 + " Exited from Application " + "----"*5)
            break
        else:
            print("Wrong Choice")

                
            
    