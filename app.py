from flask import Flask, render_template , url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'electoral_bond'

mysql = MySQL(app)

@app.route('/', methods = ['HOME','GET'])
def index():
    return render_template('index.html')

@app.route('/search_table1' , methods = ['POST','CLEAR','GET'])
def search_table1():
    if request.method == "POST":
        column = request.form['column']
        column_value = request.form['column_value']

        cursor = mysql.connection.cursor()
        cursor.execute(f"select * from `bonds encashed by political parties` where `{column}` like '{column_value}'")

        data = cursor.fetchall()

        cursor.close()
        return render_template("table1.html", data = data)
    
    else:
        return render_template("search1.html")

@app.route('/search_table2' , methods = ['POST','CLEAR','GET'])
def search_table2():
    if request.method == "POST":
        column = request.form['column']
        column_value = request.form['column_value']

        cursor = mysql.connection.cursor()
        cursor.execute(f"select * from `bonds purchased by individuals and companies` where `{column}` like '{column_value}'")

        data = cursor.fetchall()

        cursor.close()
        return render_template("table2.html", data = data)
    
    else:
        return render_template("search2.html")

@app.route('/bond_value' , methods = ['POST', 'CLEAR' ,'GET'])
def bond_value():
        
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT DISTINCT Name_of_the_Purchaser FROM `bonds purchased by individuals and companies`")
    company = cursor.fetchall()

    if request.method == 'POST':

        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT DISTINCT Name_of_the_Purchaser FROM `bonds purchased by individuals and companies`")
        company = cursor.fetchall()
        company_name = request.form['company_name']
        cursor.execute(f"SELECT YEAR(STR_TO_DATE(Date_of_Purchase, '%d/%b/%Y')) AS purchase_year,COUNT(Bond_Number) AS number_of_bonds,SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10, 0))) AS total_denominations FROM `bonds purchased by individuals and companies` WHERE (Name_of_the_Purchaser = '{company_name}') GROUP BY YEAR(STR_TO_DATE(Date_of_Purchase, '%d/%b/%Y'))")
        data = cursor.fetchall()
        xaxis = [row[0] for row in data]
        yaxis = [row[1] for row in data]
        cursor.execute(f"select count(Bond_Number) from `bonds purchased by individuals and companies` where Name_of_the_Purchaser like '{company_name}'")
        count = cursor.fetchall()
        cursor.execute(f"SELECT SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10,0))) FROM `bonds purchased by individuals and companies` where Name_of_the_Purchaser like '{company_name}'")
        value = cursor.fetchall()
        cursor.close()
        return render_template("bond_value_search_table.html", data = data , count= count, value= value , name = company_name, xaxis=xaxis,yaxis=yaxis)

    else:
         return render_template("bond_value_search.html", company_names = company)

@app.route('/political_party' , methods = ['POST', 'CLEAR' ,'GET'])
def political_party():
        
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT DISTINCT `Name of the Political Party` FROM `bonds encashed by political parties`")
    party = cursor.fetchall()

    if request.method == 'POST':

        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT DISTINCT `Name of the Political Party` FROM `bonds encashed by political parties`")
        party = cursor.fetchall()
        party_name = request.form['party_name']
        cursor.execute(f"SELECT YEAR(STR_TO_DATE(Date_of_Encashment, '%d/%b/%Y')) AS purchase_year,COUNT(Bond_Number) AS number_of_bonds,SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10, 0))) AS total_denominations FROM `bonds encashed by political parties` WHERE (`Name of the Political Party` = '{party_name}') GROUP BY YEAR(STR_TO_DATE(Date_of_Encashment, '%d/%b/%Y'))")
        data = cursor.fetchall()
        xaxis = [row[0] for row in data]
        yaxis = [row[1] for row in data]
        cursor.execute(f"select count(Bond_Number) from `bonds encashed by political parties` where `Name of the Political Party` like '{party_name}'")
        count = cursor.fetchall()
        cursor.execute(f"SELECT SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10,0))) FROM `bonds encashed by political parties` where `Name of the Political Party` like '{party_name}'")
        value = cursor.fetchall()

        cursor.close()
        return render_template("political_party_search_table.html", data = data , count= count, value= value , name = party_name , xaxis=xaxis,yaxis=yaxis)

    else:
         return render_template("political_party_search.html", party_names = party)
    

@app.route('/chart')
def chart():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT DISTINCT `Name of the Political Party` FROM `bonds encashed by political parties`")
    party = cursor.fetchall()

    money = []

    for party_name in party:
        query = "SELECT SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(10,0))) FROM `bonds encashed by political parties` WHERE `Name of the Political Party` = %s"
        cursor.execute(query, (party_name,))
        value = cursor.fetchone()
        money.append(value)

    cursor.close()

    return render_template("pie_chart.html", money=money, party=party)

    
if __name__ == "__main__":
    app.run(debug=True)