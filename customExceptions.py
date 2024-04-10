
class Empty_file_Error(Exception):
    def __str__(self):
        return "\033[1m Empty file Exception:\033[0m File does not contain any data !"
class Exceed_Quantity(Exception):
    def __str__(self):
        return "\033[1m Exceed_Quantity Exception ocurred:\033[0m Your not allowed to remove Books Quantity greater than total available Books !"
    
class Remove_Self(Exception):
    def __str__(self):
        return "\003[1m Self removing Exception Ocurred: \033[0m You cant Remove Your Self !"

class Invalid_Name(Exception):
    def __str__(self):
        return "\033[1m Invalid_Name Exception Ocurred: \033[0m UserName Should contain only characters !"