import configparser
import mysql.connector
from RANode import RANode

relations= []
colname = []
coltype = []
attributes = {}
datatypes = {}
myConnection = None
username = ''
password = ''
hostname = ''
database = ''

def dbconnection(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    global myConnection,username,password,hostname,database
    username = config['DEFAULT']['username'] 
    password = config['DEFAULT']['password'] 
    hostname = config['DEFAULT']['hostname']
    database = config['DEFAULT']['database']
    try:
        myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database )
        print("SQL connected")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err)) 

    try:
        initializeSchema()
    except mysql.connector.Error as err:
        print("Could not initialize database")
        print("Something went wrong: {}".format(err))

def initializeSchema():
    mycursor= myConnection.cursor()
    query = "select distinct table_name from information_schema.tables where table_schema='" + database + "'";
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for x in myresult:
        relations.append(x[0])
    for x in relations:
        
        colname = []
        coltype = []
        query = "select distinct column_name,column_type from information_schema.columns where table_name='" + x + "'";
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        for y in myresult:
            if y[1].startswith('int'):
                coltype.append("NUMBER")
            elif y[1].startswith( 'decimal' ):
                coltype.append("NUMBER")   
            else:
                coltype.append("STRING") 
            colname.append(y[0])
        attributes[x] = colname
        datatypes[x] = coltype

def displayDatabaseSchema():
    for x in relations:
        colname = attributes[x]
        coltype = datatypes[x]
        i=0
        print(x.upper(),"(",end=" ")
        while i < len(colname):
            print(colname[i].upper(),":",coltype[i].upper(),end=" ")
            i+=1
            if i!=len(colname):
                print(",",end=" ")
            else:
                print(")") 


def displayQueryResults(query,TreeNode):
    try:
        mycursor= myConnection.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        temp = "ANSWER("
        for x in TreeNode.schema:
            i = (TreeNode.schema).index(x)
            temp = temp + x.upper()+":"+TreeNode.dataTypes[i]+","
        temp = temp[:-1]
        print("\n"+temp+")","\n")
        print("Number of Tuples = ",len(myresult))
        for res in myresult:
            print()
            for x in range(len(res)):
                print(str(res[x])+":",end="")
        print("\n")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

