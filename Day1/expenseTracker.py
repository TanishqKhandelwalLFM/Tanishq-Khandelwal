import json

try :
    with open ("expense.json" , "r") as file :
        data = json.load(file)
except FileNotFoundError :
    print("file not exists ")
    data = []
except Exception as e :
    print(e)

def addExpense():
    title = input("Enter title of your expense ")
    amount = int(input("Enter total amount "))
    date = input("Enter date of expense ")
    keyword = input("Enter keyword where you spent ")

    expenses = {
        "id" : len(data) + 1,
        "title" : title,
        "amount" : amount,
        "date" : date,
        "keyword" : keyword
    }

    


    data.append(expenses)
    with open("expense.json","w") as file : 
        json.dump(data,file,indent=4)

def searchexpense() : 
    search = input("Enter which category you want ")

    all = []

    for d in data :
        if d['keyword'] == "food" :
            all.append(d)


    print(all)

def totalexpense() :
    sum = 0

    for d in data :
        sum += d['amount']

    print(sum)

def filterexpense() :
    expense = {}

    for d in data :
        keyword = d['keyword']

        if keyword in expense:
            expense[keyword] += d['amount']
        else:
            expense[keyword] = d['amount']

    print(expense)

def deleteExpense() :
    id = int(input("Enter expense id you want to delete "))

    for d in data :
        if d['id'] == id :
            data.remove(d)
            break
    else :
        print("not exists")

    with open("expense.json","w") as file : 
        json.dump(data,file,indent=4)


    
if __name__ == "__main__" : 
    deleteExpense()