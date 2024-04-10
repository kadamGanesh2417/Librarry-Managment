import datetime as dt
import random as rd
from User import *
from prettytable import PrettyTable as pt
from customExceptions import *

class LibraryMngt:

    def register(role):
            print("\t\t\t\t"+"==="*5+" Registering new User "+"==="*5)
            try:
                uname = input("\t\t\t\t"+ "Enter your User Name: ")
                if any(char.isdigit() for char in uname):
                    raise Invalid_Name
                password = input("\t\t\t\t"+" Enter Password: ")
                # role = "User"
                with open("users.txt",'a') as file:
                    
                    file.writelines(f"\n{uname} || {password} || {role}"+"\n")
                    print("\t\t\t\t"+" Registered successfully")
                    return True
            except Invalid_Name as inName:
                print(inName)
                       
    def login(user_name,password,role):
        with open("users.txt",'r') as ufile:
            udata = ufile.readlines()
            for udata in ufile:
                split_udata = udata.split(" || ")
                if user_name == split_udata[0] and password == split_udata[1] and split_udata[2].replace("\n",'')==role:
                    print("Credential found correct")
                    break
                    
                else: 
                    print("user not found")
                    return False  
            
    def Add_Book(self,b):
        with open("Books.txt", 'a') as file:
            file.write(str(b))
            print("\t\t Book Added Successfully ")

    def Display_books(self):
        table = pt()
        table.field_names = ["Book Id", "Book Name", "Author", "Status", "Available Copies"]

        try:
            with open("Books.txt", 'r') as file:
                print("\t\t" + "===" * 10 + " Book Register " + "===" * 10 + "\n")
                
                # Check if the file is empty
                if file.readable():
                    for book in file:
                        if not book:
                            raise Empty_file_Error
                        else:
                            book = book.strip()  # Remove leading and trailing whitespaces
                            split_book = book.split(" | ")

                        # Print the split values for debugging
                            # print("Split values:", split_book)
                            if len(split_book) == len(table.field_names):
                                table.add_row(split_book)
                            else:
                                print(True)
                            # print(f"Ignoring invalid data: {split_book}")
                else:
                    pass
        
       
            print(table)
            print("\n")
        except FileNotFoundError as error:
            print(f"Record File Not found: {error}")
        except Exception as error:
            print(f"An error occurred: {error}")
        except Empty_file_Error as e:
            print(e)

    def borrow_book(book_id, username):
        print("===" * 5 + " Borrow Book Section " + "===" * 5 + "\n")

        try:
            
            with open("Books.txt", 'r+') as file:
                b_data = file.readlines()
                for data in b_data:
                    split_bdata = data.strip().split(" | ")
                    if book_id == split_bdata[0]:
                        if int(split_bdata[4]) > 0:
                            print("book available")
                            user_input_date = input("Enter Date (dd/mm/yyyy): ")
                            try:
                                user_date = dt.datetime.strptime(user_input_date, "%d/%m/%Y").date()
                                converted_date = user_date.strftime("%d/%m/%Y")
                                return_date = "N/A"
                                fine = 0
                                print(f"Converted Date: {user_date}")
                            except ValueError:
                                print("Invalid date format. Please enter the date in the format dd/mm/yyyy.")
                            
                            new_availability = str(int(split_bdata[4]) - 1)
                            split_bdata[4] = new_availability
                            split_bdata[3] = "Not_Available" if int(split_bdata[4]) == 0 else split_bdata[3]
                            b_data[b_data.index(data)] = " | ".join(split_bdata) + '\n'
                            file.seek(0)
                            file.writelines(b_data)
                            print(f"{username} has successfully borrowed the book.")
                            issue_number = rd.randint(10,99)
                            with open("Borrowed_Register.txt",'a') as file:
                                Borrow_data = f"{issue_number} || {split_bdata[0] } || {split_bdata[1]} || {username} || {converted_date} || Borrowed || {return_date} || {fine} " +"\n"
                                file.write(Borrow_data)
                                print("borrowed Register updated !")
                                break
                        else:
                            print(f"{split_bdata[0]} is not Available")
                            break
                else:
                    print(f"book with {book_id} Not found")

                    

        except FileNotFoundError:
            print("Books.txt file not found.")
            return False

    def Return_book(book_id, username):
            
            # Update Borrowed_Register.txt
            with open("Borrowed_Register.txt", 'r+') as register_data:
                register_lines = register_data.readlines()
                for data in (register_lines):
                    split_data = data.split(" || ")
                    if split_data[3] in username:
                        print("Debug:", data)  # Debugging statement

                        if (str(split_data[0]) == str(book_id)) and (split_data[5] == "Borrowed") and (username in split_data[3]):
                            
                            issue_date = split_data[4].strip()
                            print(f"Issue Date: {issue_date}")

                            try:
                                # Convert issue_date to a date object
                                con_issue_date = dt.datetime.strptime(issue_date, '%d/%m/%Y').date()

                                # Get the current return date
                                return_date = dt.datetime.today().date()

                                # Calculate the difference in days
                                diff_days = (return_date - con_issue_date).days
                                print(f"Book '{split_data[2]}' is being returned after {diff_days} days.")

                            except ValueError as e:
                                print(f"Error converting issue_date: {e}")
                                break

                            if diff_days > 7:
                                panelty = 10 * (diff_days - 7)
                            else:
                                panelty = 0

                            pay = input(f"your penalty is RS {panelty} \nEnter 'y' to pay the amount: ")
                            if pay.lower() == "y":
                                split_data[6] = return_date.strftime("%d /%m /%Y")
                                split_data[5] = "Returned"
                                split_data[7] = str(panelty)
                                updated_line = " || ".join(split_data) + "\n"
                                register_lines[register_lines.index(data)] = updated_line
                                register_data.seek(0)
                                register_data.writelines(register_lines)
                                print("\n\tPayment Successful.\n")
                                # Update Books.txt
                                with open("Books.txt", 'r+') as books_file:
                                    book_lines = books_file.readlines()

                                    line_number = 0  # Initialize line_number variable

                                    for book_line in book_lines:
                                        book_data = book_line.strip().split(' | ')
                                        print("Debug Book:", book_data)  # Debugging statement

                                        if split_data[1] == str(book_data[0]):
                                            book_data[4] = str(int(book_data[4]) + 1)
                                            if str(int(book_data[4])>0):
                                                book_data[3] = "Available" 
                                            book_lines[line_number] = " | ".join(book_data) + "\n"
                                            books_file.seek(0)
                                            books_file.writelines(book_lines)
                                            books_file.truncate()
                                            print("Books Data Updated!")
                                            return True

                                        line_number += 1  # Increment line_number

                                print(f"Book Issued ID {book_id} not found.")
                                return False
                                return True  # Return True if everything is successful
                            else:
                                print("Book Not Returned ")
                                return False
                
                # If the loop completes without finding the book, print a message
                print(f"Book with ID {book_id} is not found or is already returned.")
                return False

    def Get_Borrowed_Book():
        print("\t\t\t\t"+"==="*5 + " Borrowed Books " + "==="*5+"\n")
        print(""+" Book ID ||  Book Name  ||  Username  ||  Issue date || Status || Return date || Fine \n" )
        try:
            with open("Borrowed_Register.txt", "r") as file:
                books = file.readlines()
                if not books:
                    raise EmplyfileError
                for line in books:
                    data = line.split(" || ")  
                    if data[4] == "Borrowed":
                        print(f" {data[0]} | {data[1]} | {data[2]} | {data[3]} | {data[4]} | {data[5]} | {data[6]}")  


        except FileNotFoundError:
            print("Error: File 'Books.txt' not found!")
        except EmplyfileError as em:
            print(em)
            
    def Search_Book():
        print("\t\t\t\t"+"-----"*5+" Search Book "+"-----"*5)
        Bid_bname = input("\t\t\t\tSearch by Bookid , Book_name , Author: ")+"\n"
        if Bid_bname.endswith("\n"):
            Bid_bname = Bid_bname.replace("\n","")
        with open("Books.txt", "r")as Brecords:
            Bdata = Brecords.readlines()
            for line in Bdata:
                data = line.split(" | ") 
                if len(data)>1:

                    if (
                        Bid_bname in data[0] or  
                        Bid_bname in data[2] or 
                        Bid_bname in (data[1])
                        ):
                    # if Bid_bname in data:
                        print("\t\t Here Is your Data: \n"+"-----"*4)
                        print(f"\t\tID: {data[0]} \n\t\tName: {data[1]}\n\t\tAuthor: {data[2]}\n\t\tCopies Available: {data[4]}" +"-----"*4)
                        
                    # else:
                    #     pass
            else:
                print("\t\tNot Found")
        
    def Get_Available_Books(self):
        table = pt()
        table.field_names = ["Book id", "Book Name", "Book Author"]
        print("===" * 5 + " Available Books " + "===" * 5)
        try:
            with open("Books.txt", "r") as file:
                books = file.readlines()
                for line in books:
                    data = line.split(" | ")  
                    if len(data)>0 and int(data[4]) > 0:
                        split_cols = data[0:3]
                        table.add_row(split_cols)
                    else:
                        pass
            if table.rows:
                print(table)
            else:
                raise Empty_file_Error
            
        except Empty_file_Error as emt:
            print(f"{emt}")
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def delete_book(book_identifier):
        print("\t\t\t\t"+"===" * 5 + " Delete Book Section " + "===" * 5)
        try:
            # Check if the book is borrowed
            with open("Borrowed_Register.txt", "r") as register_file:
                register_lines = register_file.readlines()
                if not register_lines:
                    pass
                else:
                    for line in register_lines:
                        data = line.split(" || ")
                        if data[0] == str(book_identifier) and data[4] == "Borrowed":
                            print(f"\t\t\t\tCannot delete the book. Book '{data[1]}' is currently borrowed.")
                        
                            return False
                        
            # If it's not borrowed, then we can proceed to deletion
                       

                    with open("Books.txt",'r') as file:
                        books_data = file.readlines()
                    books_data = [data  for data in books_data if book_identifier not in data]

                    with open("Books.txt",'w') as override_data:
                        override_data.writelines(books_data)
                        print(f"\t\t\t\tBook with Id {book_identifier} is Removed from library")
                        return True    

           

        except FileNotFoundError:
            print("Error: File not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def Remove_Admin(Admin,uersname):
        try: 
            if Admin == uersname:
                raise Remove_Self
            else:
                with  open("users.txt", "r") as file:
                    users=file.readlines()
                    
                    for d in users:
                        if d.endswith("\n"):
                            d = d.replace("\n","")
                        filtered_d = d.split(" || ")
                        if Admin==filtered_d[0] and filtered_d[2]=="Admin":
                            print(f"{Admin} Found ")
                            updated_admin = [d for d in users if not d.startswith(Admin)]
                            with open("users.txt","w") as Updated_Admins:
                                Updated_Admins.writelines(updated_admin)
                            
                            print(f"{Admin} has been removed from the admin list.")
                            break
                        
                        else:
                            pass
                    else:
                        print(f"{Admin} Not Found in Admin List!")  
        except  Remove_Self as r:
            print(r)              

    def update_book(book_name):
        try:
            with open("Books.txt",'r+') as file:
                book_data = file.readlines()
                if not book_data:
                    raise Empty_file_Error
                else:
                    for book in book_data:
                        split_book_data = book.split("|")
                        if (book_name in split_book_data[0]) or (book_name in split_book_data[1]) :
                            print("Book Found")
                            user_choice = input("Enter\nN for update book name\nA for update Author\nQ for update Available Books\nYour Choice: ")
                            if user_choice.upper()=='N':
                                new_name = input("New Book Name: ")
                                old_name = split_book_data[1]
                                split_book_data[1]=new_name
                                updated_data = " | ".join(split_book_data)
                                book_data[book_data.index(book)] = updated_data
                                file.seek(0)
                                file.writelines(book_data)
                                print(f"{old_name} is Updated to {new_name}")
                                break
                            elif user_choice.upper()=='A':
                                new_Author = input("New Author: ")
                                split_book_data[2]=new_Author
                                updated_data = " | ".join(split_book_data)
                                book_data[book_data.index(book)] = updated_data
                                file.seek(0)
                                file.writelines(book_data)
                                print(f"{split_book_data[2]} is Updated to {new_Author}")
                                break
                            elif user_choice.upper()=="Q":
                                uip = input("A for Add more copies to the book\nR for remove copies from book : ")
                                if uip =='A':
                                    qty = int(input("Copies: "))
                                    split_book_data[4] = str(int(split_book_data[4])+qty)
                                    updated_data = " | ".join(split_book_data)
                                    book_data[book_data.index(book)] = updated_data
                                    file.seek(0)
                                    file.writelines(book_data)
                                    print(f"Copies of {split_book_data[1]} is updated to {split_book_data[4]}")
                                elif uip == 'R':
                                    qty = int(input("Remove Copies:  "))
                                    curr_copies = int(split_book_data[4])
                                    if curr_copies <  qty:
                                        raise Exceed_Quantity
                                        
                                    else:
                                        split_book_data[4] = str(int(split_book_data[4])- qty)
                                        updated_data = " | ".join(split_book_data)
                                        book_data[book_data.index(book)] = updated_data
                                        file.seek(0)
                                        file.writelines(book_data)
                                        print(f"Copies of {split_book_data[1]} is Updated to {split_book_data[4]}")
                                        break
            
                        else:
                            print("Wrong Choice")
        except Exceed_Quantity as Inv:
            print(f"Error Ocurred: {Inv}")
        except Empty_file_Error as empty:
            print(f"Error Occured : {empty}")
    
    def get_Fine_data():
        pass