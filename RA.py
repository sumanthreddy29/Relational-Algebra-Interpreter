import sys
import ply.yacc as yacc
from RAParser import parser
from MySQL import *
from RANode import RANode
counter = 0

def semanticChecks(TreeNode):
    if TreeNode.node_type == 'relation':
        if TreeNode.relationName not in relations:
            return TreeNode.relationName + " does not exist"
        TreeNode.schema = attributes[TreeNode.relationName]
        TreeNode.dataTypes = datatypes[TreeNode.relationName]
        return 'OK'
    if TreeNode.node_type == 'union' or TreeNode.node_type == 'minus' or TreeNode.node_type == 'intersect':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        str2 = semanticChecks(TreeNode.right)
        if str2 != 'OK':
            return str2
        arrayList4 = TreeNode.left.schema
        arrayList5 = TreeNode.left.dataTypes
        arrayList6 = TreeNode.right.schema
        arrayList7 = TreeNode.right.dataTypes
        if len(arrayList4) != len(arrayList6):
            return 'tables are not the same size'
        for x in arrayList5:
            if x not in arrayList7:
                return "Columns do not have the same data types"
        TreeNode.schema = arrayList4
        TreeNode.dataTypes = arrayList5
        return "OK"

    if TreeNode.node_type == 'times':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        str2 = semanticChecks(TreeNode.right)
        if str2 != 'OK':
            return str2
        arrayList4 = TreeNode.left.schema
        arrayList5 = TreeNode.left.dataTypes
        arrayList6 = TreeNode.right.schema
        arrayList7 = TreeNode.right.dataTypes
        schema = []
        dataTypes = []
        for x in arrayList4:
        	i = arrayList4.index(x)
        	if x in arrayList6:
        		scehma.append(TreeNode.left.relationName+"."+x)
        	else:
        		schema.append(x)
        		dataTypes.append(arrayList5[i])
        for x in arrayList6:
        	i = arrayList6.index(x)
        	if x in arrayList4:
        		scehma.append(TreeNode.right.relationName+"."+x)
        	else:
        		schema.append(x)
        		dataTypes.append(arrayList7[i])
        TreeNode.schema = schema
        TreeNode.dataTypes = dataTypes
        return "OK"

    if TreeNode.node_type == 'join':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        str2 = semanticChecks(TreeNode.right)
        if str2 != 'OK':
            return str2
        arrayList4 = TreeNode.left.schema
        arrayList5 = TreeNode.left.dataTypes
        arrayList6 = TreeNode.right.schema
        arrayList7 = TreeNode.right.dataTypes

        schema = []
        dataTypes = []
        joinColumns = []

        for x in arrayList4:
            i = arrayList4.index(x)
            schema.append(x)
            dataTypes.append(arrayList5[i])
            if x in arrayList6:
                joinColumns.append(x)
        for x in arrayList6:
            i = arrayList6.index(x)
            if x not in arrayList4:
                schema.append(x)
                dataTypes.append(arrayList7[i])

        TreeNode.schema = schema
        TreeNode.dataTypes = dataTypes
        TreeNode.joinColumns = joinColumns
        return "OK"

    if TreeNode.node_type == 'project':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        arrayList4 = TreeNode.attribute_list
        
        arrayList5 = TreeNode.left.schema
        arrayList6 = TreeNode.left.dataTypes
        arrayList7 = []
        for x in arrayList4:
            if(x not in arrayList5):
                return x+" is not a valid attribute"
        for x in arrayList4:
            i=arrayList5.index(x)
            arrayList7.append(arrayList6[i])
        TreeNode.schema = arrayList4
        TreeNode.dataTypes = arrayList7
        return "OK"
        #print(arrayList4,arrayList5,arrayList6)
    if TreeNode.node_type == 'rename':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        arrayList4 = TreeNode.attribute_list
        arrayList5 = TreeNode.left.schema
        arrayList6 = TreeNode.left.dataTypes
        if len(arrayList5) != len(arrayList4):
            return "Not a valid amount of attributes"
        TreeNode.schema = arrayList4
        TreeNode.dataTypes = arrayList6
        return "OK"
        #print(arrayList4,arrayList5,arrayList6)
    if TreeNode.node_type == 'select':
        str1 = semanticChecks(TreeNode.left)
        if str1 != 'OK':
            return str1
        arrayList4 = TreeNode.left.schema
        arrayList5 = TreeNode.left.dataTypes
        arrayList6 = TreeNode.condition 
        #print(arrayList4,arrayList5,arrayList6)
        for x in arrayList6:
            leftOperand = x[0]
            leftDataType = x[1]
            rightOperand = x[3]
            rightDataType = x[4]
            if leftOperand not in arrayList4:
                return leftOperand+" is not a valid operand"
            i = arrayList4.index(leftOperand)
            leftDataType = arrayList5[i]
            if leftDataType == 'STRING':
                leftDataType = type('str')
            else:
                leftDataType = type(123)
            if leftDataType != rightDataType:
                return "Data types does not match"
        TreeNode.schema = arrayList4
        TreeNode.dataTypes = arrayList5
        return "OK"

def populateRelationNames(TreeNode):
  global counter
  if TreeNode.node_type is not 'relation':
    if isinstance(TreeNode,type(TreeNode.left)):
        populateRelationNames(TreeNode.left)
    if isinstance(TreeNode,type(TreeNode.right)):
        populateRelationNames(TreeNode.right)
    TreeNode.relationName = "temp"+str(counter)
    counter = counter + 1
  #print(TreeNode.relationName,TreeNode.node_type)

def generateSQL(TreeNode):
    if TreeNode.node_type == 'relation':
        return "(select * from "+TreeNode.relationName+")"
    if TreeNode.node_type == 'union':
        str1 = generateSQL(TreeNode.left)
        str2 = generateSQL(TreeNode.right)
        return str1+" union "+str2
    if TreeNode.node_type == 'project':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        query = "(select distinct "
        arraylist1 = TreeNode.attribute_list
        for x in arraylist1:
        	query =  query + TreeNode.left.relationName + "."+ x + ","
        query = query[:-1]
        query = query + " from "+str1+" "+ TreeNode.left.relationName + ")"
        return query
    if TreeNode.node_type == 'rename':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        query = "(select "
        arraylist1 = TreeNode.attribute_list
        for x in arraylist1:
        	i = arraylist1.index(x)
        	query =  query +TreeNode.left.schema[i]+" "+ x + ","
        query = query[:-1]
        query = query + " from "+str1+" "+ TreeNode.left.relationName + ")"
        return query
    if TreeNode.node_type == 'select':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        query = "(select * from "+str1+" "+TreeNode.left.relationName+" where "
        arraylist1 = TreeNode.condition
        for x in arraylist1:
            query =  query + str(x[0]) + str(x[2]) + str(x[3]) + " and "
        query = query[:-4]
        query = query + ")"
        
        return query
    if TreeNode.node_type == 'intersect':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        str2 = generateSQL(TreeNode.right)
        if TreeNode.right.node_type == 'union':
            str2 = "("+str2+")"
        query = "(select * from "+ str1 + " " +TreeNode.left.relationName+" where ("
        arrayList1 = TreeNode.schema
        for x in arrayList1:
            query = query + x + ","
        query = query[:-1]
        query = query + ") in "
        query = query + "(select * from "+str2+" "+TreeNode.right.relationName+"))"
        return query
    if TreeNode.node_type == 'times':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        str2 = generateSQL(TreeNode.right)
        if TreeNode.right.node_type == 'union':
            str2 = "("+str2+")"
        query = "(select * from "+ str1 + " " +TreeNode.left.relationName+", "
        query = query+str2+" "+TreeNode.right.relationName+")"
        return query

    if TreeNode.node_type == 'minus':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        str2 = generateSQL(TreeNode.right)
        if TreeNode.right.node_type == 'union':
            str2 = "("+str2+")"
        query = "(select * from "+ str1 + " " +TreeNode.left.relationName+" where ("
        arrayList1 = TreeNode.schema
        for x in arrayList1:
            query = query + x + ","
        query = query[:-1]
        query = query + ") not in "
        query = query + "(select * from "+str2+" "+TreeNode.right.relationName+"))"
        return query

    if TreeNode.node_type == 'join':
        str1 = generateSQL(TreeNode.left)
        if TreeNode.left.node_type == 'union':
            str1 = "("+str1+")"
        str2 = generateSQL(TreeNode.right)
        if TreeNode.right.node_type == 'union':
            str2 = "("+str2+")"
        query = "(select distinct "
        arrayList1 = TreeNode.schema
        for x in arrayList1:
            if x in TreeNode.joinColumns:
                query = query + TreeNode.left.relationName +"."+x+","
            else:
                query = query + x+","
        query = query[:-1]
        query = query + " from "+str1+" "+TreeNode.left.relationName+", "+str2+" "+TreeNode.right.relationName+" "
        if len(TreeNode.joinColumns) == 0:
        	return query+")"
        query = query + " where "
        for x in TreeNode.joinColumns:
        	query = query + TreeNode.left.relationName+"."+x+"="+TreeNode.right.relationName+"."+x+" and "
        query = query[:-4]
        query = query + ")"
        return query

def read_inputfile(fileName):
    f = open(fileName, "r")
    s = ''
    with open(fileName) as f:
        line = f.readline()
        while line:
            if line[0] == '/' and line[1]=='/':
                print("")
            else:
                s +=line
            line = f.readline()

    return s

def read_input():
    s = ""
    while True:
        print('RA> ', end='', flush=True)
        s1 = sys.stdin.readline().strip()
        if s1 == 'clr;':
            s= ""
        else:
            s += s1
            if s != '':
                if s[-1] == ";":
                    break
                s += ' '
    return s

def main():
  query_print = False
  if(len(sys.argv) == 2):
      dbconnection(sys.argv[1])
  else:
      query_print = True
      dbconnection(sys.argv[2])
  while True:
    s = read_input()
    if s[0:len(s)-1].strip() == 'exit':
      break
    elif(s == 'SCHEMA;' or s == 'schema;'):
      displayDatabaseSchema()
    elif s.startswith("source"):
        s=read_inputfile(s[7:-1])
    if s != '':
        tree = parser.parse(s.strip())
        if tree != None :
            status = semanticChecks(tree)
            if status == "OK":
                populateRelationNames(tree)
                query = generateSQL(tree)
                if query_print :
                    print("Query:",query,"\n")
                displayQueryResults(query,tree)
            else:
                print(status)

main()
