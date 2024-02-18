import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur  = conn.cursor()

while True:
    print("Select a n option :")
    print("1. Enter a new expense")
    print("2. View your expenses")
    
    choice = int(input())
    
    if choice ==1:
        date = input("enter the date of expense(YYYY-MM-DD):")
        description = input("Enter the description of expense: ")
        
        cur.execute("SELECT DISTINCT category FROM expenses")
        
        categories = cur.fetchall()
        print("Select a categor by number: ")
        for idx, category in enumerate(categories):
            print(f"{idx+1}. {category[0]}")
        print(f"{len(categories)+1}. Create a new category")
        
        category_choice =int(input())
        if category_choice == len(categories)+1:
           category = input("Enter a new category: ")
        else :
            category = categories[category_choice-1][0] 
        
        price = input("Enter the price of expense: ")
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES(?,?,?,?)",(date, description,category,price))
        
        conn.commit()
        

        
    elif choice == 2:
        print("Select a option: ")
        print("1. View all expenses")
        print("2. View all expenses by category")
        print("3. View monthly expenses")
        print("4. View yearly expenses")
        view_choice = int(input())
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            cur.execute("SELECT DISTINCT category FROM expenses")
            categories = cur.fetchall()

            print("Select a category by number:")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category[0]}")

            category_choice = int(input())
            selected_category = categories[category_choice - 1][0]

            cur.execute("""SELECT * FROM expenses
                           WHERE category = ?""", (selected_category,))

            expenses_by_category = cur.fetchall()

            print(f"\nExpenses for category '{selected_category}':")
            for expense in expenses_by_category:
                print(expense)

            cur.execute("""SELECT SUM(price) FROM expenses
                           WHERE category = ?""", (selected_category,))

            total_expense = cur.fetchone()[0]
            print(f"\nTotal expense for category '{selected_category}': {total_expense}")
        
        elif view_choice == 3:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cur.execute("""SELECT * FROM expenses
                           WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?""", (month, year))

            monthly_expenses = cur.fetchall()

            print(f"\nExpenses for {datetime.date(int(year), int(month), 1).strftime('%B %Y')}:")
            for expense in monthly_expenses:
                print(expense)

            cur.execute("""SELECT SUM(price) FROM expenses
                           WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?""", (month, year))

            total_expense = cur.fetchone()[0]
            print(f"\nTotal expense for {datetime.date(int(year), int(month), 1).strftime('%B %Y')}: {total_expense}")

        elif view_choice == 4:
            year = input("Enter the year (YYYY): ")
            cur.execute("""SELECT * FROM expenses
                   WHERE strftime('%Y', Date) = ?""", (year,))

            yearly_expenses = cur.fetchall()

            if not yearly_expenses:
                print(f"\nNo expenses recorded for the year {year}")
            else:
                print(f"\nExpenses for the year {year}:")
            for expense in yearly_expenses:
                print(expense)

            cur.execute("""SELECT SUM(price) FROM expenses
                       WHERE strftime('%Y', Date) = ?""", (year,))

            total_expense = cur.fetchone()[0]
            print(f"\nTotal expense for the year {year}: {total_expense}")

        else:
            exit()
    else:
        exit()
            
    repeat = input("Would you like to do something else(y/n): ")
    if repeat.lower()!='y':
        break
conn.close()