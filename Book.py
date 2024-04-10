class Book:
    def __init__(self,Bid,Bname,Author,Status,copy) -> None:
        self.Bid = Bid
        self.Bname = Bname
        self.Author = Author
        self.Status = "Available"
        self.copy = copy
    
    
    def __str__(self) -> str:
        return f"{str(self.Bid)} | {self.Bname} | {self.Author} | {self.Status}  |  {self.copy} \n"   
        