import ply.yacc as yacc
from RALexer import tokens
from RANode import RANode

precedence = ( 
  ("left", "UNION", "MINUS", "INTERSECT"),
  ("left", "JOIN", "TIMES"),
)

def p_query(t):
  'query : expression SEMICOLON'
  t[0] = t[1]

def p_expression_select(t):
  'expression : SelectExpr'
  t[0] = t[1]

def p_expression_project(t):
  'expression : ProjectExpr'
  t[0] = t[1]

def p_expression_rename(t):
  'expression : RenameExpr'
  t[0] = t[1]  

def p_expression_union(t):
  'expression : UnionExpr'
  t[0] = t[1]

def p_expression_minus(t):
  'expression : MinusExpr'
  t[0] = t[1]

def p_expression_intersect(t):
  'expression : IntersectExpr'
  t[0] = t[1]

def p_expression_join(t):
  'expression : JoinExpr'
  t[0] = t[1]

def p_expression_times(t):
  'expression : TimesExpr'
  t[0] = t[1]

def p_expression_name(t):
  'expression : NAME'
  node = RANode()
  node.node_type = "relation"
  node.relationName = t[1].lower()
  t[0] = node

def p_expression_parenth(t):
  'expression : LPAREN expression RPAREN'
  t[0] = t[2]

def p_SelectExpr(t):
  'SelectExpr : SELECT SLPAREN condition SRPAREN LPAREN expression RPAREN'
  node = RANode()
  node.left = t[6]
  node.node_type = "select"
  node.right = None
  node.condition = t[3]
  t[0] = node 
    
def p_ProjectExpr(t):
  'ProjectExpr : PROJECT SLPAREN AttrList SRPAREN LPAREN expression RPAREN '
  node = RANode()
  node.left = t[6]
  node.node_type = "project"
  node.right = None
  node.attribute_list=t[3]
  t[0] = node
   
def p_RenameExpr(t):
  'RenameExpr : RENAME SLPAREN AttrList SRPAREN LPAREN expression RPAREN '
  node = RANode()
  node.left = t[6]
  node.node_type = "rename"
  node.right = None
  node.attribute_list=t[3]
  t[0] = node
    
def p_AttrList_1(t):
  'AttrList : NAME'
  t[0] = [t[1]]
   
def p_AttrList_2(t):
  'AttrList : AttrList COMMA NAME'
  t[0] = t[1]+[t[3]] 
        
def p_UnionExpr(t):
  'UnionExpr : expression UNION expression'
  #t[0] = ['union',t[1],t[3]] 
  node = RANode()
  node.left = t[1]
  node.right = t[3]
  node.node_type = "union"
  t[0] = node

def p_MinusExpr(t):
  'MinusExpr : expression MINUS expression'
  t[0] = ['minus',t[1],t[3]]
  node = RANode()
  node.left = t[1]
  node.right = t[3]
  node.node_type = "minus"
  t[0] = node

def p_IntersectExpr(t):
  'IntersectExpr : expression INTERSECT expression'   
  #t[0] = ['intersect',t[1],t[3]] 
  node = RANode()
  node.left = t[1]
  node.right = t[3]
  node.node_type = "intersect"
  t[0] = node 

def p_JoinExpr(t):
  'JoinExpr : expression JOIN expression'
  t[0] = ['join',t[1],t[3]]
  node = RANode()
  node.left = t[1]
  node.right = t[3]
  node.node_type = "join"
  t[0] = node 

def p_TimesExpr(t):
  'TimesExpr : expression TIMES expression'  
  t[0] = ['times',t[1],t[3]] 
  node = RANode()
  node.left = t[1]
  node.right = t[3]
  node.node_type = "times"
  t[0] = node

def p_condition_1(t):
  'condition : simpleCondition'
  t[0] = [t[1]]

def p_condition_2(t):
  'condition : condition AND simpleCondition'
  t[0] = t[1]+[t[3]]       
    
def p_simpleCondition_op(t):
  'simpleCondition : operand COMPARISON operand'
  simplecond=(t[1],type(t[1]),t[2],t[3],type(t[3]))
  t[0]=simplecond

def p_operand_1(t):
  'operand : NAME'
  t[0] = t[1] 

def p_operand_2(t):
  'operand : STRING'
  t[0] = t[1] 

def p_operand_3(t):
  'operand : NUMBER'
  t[0] = t[1]

def p_error(t):
  if t:
    print("Syntax error at '%s'" % t.value)
  else:
    print("Syntax error at EOF")

parser = yacc.yacc()
