
class RANode:

    def __init__(self):

        self.left = None
        self.right = None        
        self.node_type = None
        self.condition = []
        self.attribute_list = []
        self.relationName= None
        self.schema=[]
        self.datatypes=[]
        self.joinColumns = []
                    

    """def PrintTree(self,level):
        
        print('\t' * level,self.node_type),
        if(self.node_type=="project" or self.node_type=="rename"):
            print('\t' * (level),self.attribute_list)
        if(self.node_type=="select"):
            print('\t' * (level-3),self.condition)     
        if isinstance(self.left, RANode):
            #print("left")   
            self.left.PrintTree(level-5)
        else:
            #print("left")
            print('\t' * (level-5),self.left)    
           
        if isinstance(self.right, RANode):
            #print("right")            
            self.right.PrintTree(level+5)
        else:
            #print("right")
            print('\t' * (level+5),self.right) """ 
            
    
    

                           

