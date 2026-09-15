# Syntecxhub_Budgeting_Program
A simple CLI program that logs your transactions entered into program, stores, run scenarios, and build a report on spending habits

The Budget Simulator is a simple Python program that helps users manage their personal finances. It uses NumPy arrays to store and calculate financial transactions. The program includes four account types: Income, Expenses, Savings, and Investments.

Users can add new transactions, edit recent transactions, clear account balances, remove accounts, or create new accounts. Each transaction includes a date and time so the user can track when it was made. The program also keeps an activity log that records important actions during the session.

The program calculates total income, expenses, savings, investments, and the remaining balance. It can also analyze spending by calculating the average and standard deviation. These calculations help the user understand spending habits and identify changes in financial behavior.

The investment feature estimates future investment value. It uses the current investment balance, expected annual return, number of years, and optional monthly contributions. This helps users understand how their investments may grow over time.

The program also includes a scenario feature. This allows the user to test possible changes, such as increasing expenses by 10% or decreasing them by 5%. The program shows the previous total, new total, and difference.

Finally, the program can create a monthly report in JSON format. The report summarizes monthly income, expenses, savings, investments, transaction counts, averages, highest and lowest transactions, and net cash flow. All data is currently stored in memory, so it is removed when the program closes.

#SHORTCOMINGS
-My idea of a fully functional program wasn't achieved, with some functionalities being half baked such as not being able to save progress.
-On the statistical end, it is too simplified and math calculations narrow

#MY OVERALL TAKE
Exciting idea to build my NumPy project, seeing that it is my first time experiencing this program. Looking forward to building more on this project 

