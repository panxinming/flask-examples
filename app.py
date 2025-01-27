
# import necessary package.
from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)



def get_message_db():
    # create a database which contains our messages.
    g.message_db = sqlite3.connect("message_db.sqite") 
    cursor = g.message_db.cursor()   
    # SQL command CREATE a TABLE called messages IF NOT EXISTS
    cursor.execute("create table if not exists messages(Id integer, handle text, message text)") 
    cursor.close()
    # Return the connection 
    return g.message_db
    

def insert_message(request):
    # collect the user's message and handle.
    message = request.form['message']
    handle = request.form['user']
    # insert message into our database.
    cursor = g.message_db.cursor()
    # insert handle, message together.
    g.sql = "INSERT INTO messages (message, handle) VALUES (?, ?)",(message, handle)        
    cursor.execute(g.sql)
    #  it is necessary to run db.commit() after inserting a row into db in order to ensure that your row insertion has been saved.
    g.message_db.commit()
    # close our database.
    cursor.close()
    g.message_db.close()



def random_messages(n):
    # connect to our database we just create.
    g.message_db = sqlite3.connect("message_db.sqite") 
    cursor = g.message_db.cursor()
    # extract what we need.
    cursor.execute("select message,handle from messages")
    # get our text
    result = cursor.fetchmany(n)
    # close our database
    cursor.close()
    g.message_db.close()
    return result


@app.route("/")
def main():
    # main page is base.html
    return render_template("base.html")


@app.route('/view/', methods=['POST', 'GET'])
def view():
    if request.method == 'GET':
        # reurn view.html if we get something.
        return render_template('view.html')
    else:
        try:
            # extract our message from database.
            g.result = random_messages(int(request.form['number']))
            # view sepcific number of messages we want to show. And return us a thank you message.
            return render_template('view.html',number = "thank you for submitting the message!")
        except:
            return render_template('view.html',number= "error")


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        # return submit.html.
        return render_template('submit.html')
    else:
        try:
            # create database.
            get_message_db()
            # insert our message into database.
            insert_message(request)
            return render_template('submit.html', user=request.form['user'], message=request.form['message'])
        except:
            return render_template('submit.html', user='error', message='error')


if __name__ == '__main__':
    app.run()