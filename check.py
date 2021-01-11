import re
class validations:
    def __init__(self,username,password,phone_number,email):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email = email
    
    def validate(self):
        """ checking for valid entries """
        
        if len(self.username) <= 0 and len(self.username) >= 9:
            return "Invalid username!! Please choose a valid username of length 1 to 8."

        elif not re.match("^[9876][0-9]{9}",self.phone_number):
       
            return "Invalid phone number."

        elif not re.match(".+@.+[.].+",self.email):

            return "Invalid email. Please enter in format a@b.c"
        
        elif not re.match("^(?=.*?[aA-zZ])(?=.*?[0-9])(?=.*?[-_#]).{6,}$",self.password):
            return "Invalid password, Password must be of length six with\
             a number and a special character from [-_#]"
        else:
            return True