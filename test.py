def isOdd(func):
    def wrapper(*args):
        sum = 0
        if func(*args) %2 == 0:
            
            print("Summing of this",len(args),"numbers is",func(*args))
            print("So its Even")
        else:

            print("Summing of this",len(args),"numbers is",func(*args))
            print("So its Even")

        return func(*args)
    
    return wrapper


@isOdd
def addition(num1:int, num2:int):
    return num1 + num2


import jwt
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imtha2VuIiwiaWQiOiI2NjdlYTk0ZGYxZTgyNjlmZjIwZGQwNTEiLCJleHAiOjE3MTk1Nzg4MTR9.mAR0xV-GfAycmKtilC5w8KE4tEPYsElZKtXE3QYFK7c'
decoded = jwt.decode(token, options={"verify_signature": False}) # works in PyJWT >= v2.0
print (decoded)
