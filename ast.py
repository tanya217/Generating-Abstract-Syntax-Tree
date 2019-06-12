'''
Parse tree for the following program,
        int main()
        { int a=0, b=10;
          while(b>0)
                {
                    if(b<2)
                        {
                            a+=1;
                        }
                    else
                        {
                            break;
                        }
                }

        }
'''


from collections import OrderedDict
import re
from nltk import Tree
parse_tree={'Symbol': 'PROGRAM', 'children': [{'Symbol': 'DECL', 'children': [{'Symbol': 'TYPE', 'children': [{'buf': 'int', 'num': 7, 'type': 'int', 'children': [], 'str': 'int'}]}, {'Symbol': 'VARLIST', 'children': [{'buf': 'a', 'num': 0, 'type': 'id', 'children': [], 'str': 'a'}, {'buf': ';', 'type': ';', 'children': []}]}]}, {'Symbol': 'FUNCDEFN', 'children': [{'buf': 'int', 'num': 7, 'type': 'int', 'children': [], 'str': 'int'}, {'buf': 'main', 'num': 20, 'type': 'main', 'children': [], 'str': 'main'}, {'buf': '(', 'type': '(', 'children': []}, {'buf': ')', 'type': ')', 'children': []}, {'Symbol': 'CSTMT', 'children': [{'Symbol': 'STMT', 'children': []}, {'buf': '{', 'type': '{', 'children': []}, {'Symbol': 'STMT', 'children': [{'Symbol': 'STMT', 'children': [{'Symbol': 'STMT', 'children': []}, {'Symbol': 'S', 'children': [{'Symbol': 'DECL', 'children': [{'Symbol': 'TYPE', 'children': [{'buf': 'int', 'num': 7, 'type': 'int', 'children': [], 'str': 'int'}]}, {'Symbol': 'ASSIGNEXPR', 'children': [{'buf': 'b', 'num': 1, 'type': 'id', 'children': [], 'str': 'b'}, {'buf': '=', 'type': '=', 'children': []}, {'Symbol': 'E', 'children': [{'Symbol': 'T', 'children': [{'Symbol': 'F', 'children': [{'buf': '0', 'num': 0, 'type': 'num', 'children': [], 'str': 0}]}]}]}, {'buf': ';', 'type': ';', 'children': []}]}]}]}]}, {'Symbol': 'S', 'children': [{'Symbol': 'SELECTIONSTMT', 'children': [{'buf': 'if', 'num': 0, 'type': 'if', 'children': [], 'str': 'if'}, {'buf': '(', 'type': '(', 'children': []}, {'Symbol': 'COND', 'children': [{'Symbol': 'BE', 'children': [{'Symbol': 'BT', 'children': [{'Symbol': 'BF', 'children': [{'Symbol': 'E', 'children': [{'Symbol': 'T', 'children': [{'Symbol': 'F', 'children': [{'buf': 'a', 'num': 0, 'type': 'id', 'children': [], 'str': 'a'}]}]}]}, {'buf': '<', 'type': 'rop', 'children': [], 'str': '<'}, {'Symbol': 'E', 'children': [{'Symbol': 'T', 'children': [{'Symbol': 'F', 'children': [{'buf': '1', 'num': 0, 'type': 'num', 'children': [], 'str': 1}]}]}]}]}]}]}]}, {'buf': ')', 'type': ')', 'children': []}, {'Symbol': 'CSTMT', 'children': [{'Symbol': 'STMT', 'children': []}, {'buf': '{', 'type': '{', 'children': []}, {'Symbol': 'STMT', 'children': [{'Symbol': 'STMT', 'children': []}, {'Symbol': 'S', 'children': [{'Symbol': 'DECL', 'children': [{'Symbol': 'TYPE', 'children': [{'buf': 'int', 'num': 7, 'type': 'int', 'children': [], 'str': 'int'}]}, {'Symbol': 'ASSIGNEXPR', 'children': [{'buf': 'c', 'num': 2, 'type': 'id', 'children': [], 'str': 'c'}, {'buf': '=', 'type': '=', 'children': []}, {'Symbol': 'E', 'children': [{'Symbol': 'T', 'children': [{'Symbol': 'F', 'children': [{'buf': '0', 'num': 0, 'type': 'num', 'children': [], 'str': 0}]}]}]}, {'buf': ',', 'type': ',', 'children': []}, {'Symbol': 'ASSIGNEXPR', 'children': [{'buf': 'd', 'num': 3, 'type': 'id', 'children': [], 'str': 'd'}, {'buf': '=', 'type': '=', 'children': []}, {'Symbol': 'E', 'children': [{'Symbol': 'T', 'children': [{'Symbol': 'F', 'children': [{'buf': '0', 'num': 0, 'type': 'num', 'children': [], 'str': 0}]}]}]}, {'buf': ';', 'type': ';', 'children': []}]}]}]}]}]}, {'buf': '}', 'type': '}', 'children': []}]}]}]}]}, {'buf': '}', 'type': '}', 'children': []}]}]}]}




grammar=[
			"PROGRAM-> FUNCDEFN ~~ stack['program_node'].append(stack['funcdefn_node'].pop()) |\
					   DECL FUNCDEFN ~~ stack['program_node'].append(newNode('program',[stack['decl_node'].pop(),stack['funcdefn_node'].pop()]))",
			"FUNCDEFN-> int main() CSTMT ~~ stack['funcdefn_node'].append(newNode('main',[newLeafNode('type','int'),stack['cstmt_node'].pop()]))",
			"CSTMT->STMT { STMT } ~~ stack['cstmt_node'].append(newNode('cstmt',[stack['stmt_node'].pop(-2),stack['stmt_node'].pop()]))",
            "STMT->STMT S ~~ stack['stmt_node'].append(newNode('stmt',[stack['stmt_node'].pop(),stack['s_node'].pop()])) |\
                   epsilon ~~ stack['stmt_node'].append(None)",
			"S->ASSIGNEXPR ~~ stack['s_node'].append(stack['assignexpr_node'].pop()) |\
                DECL ~~ stack['s_node'].append(stack['decl_node'].pop()) |\
                while (COND) CSTMT ~~ stack['s_node'].append(newNode('while',[stack['cond_node'].pop(),stack['cstmt_node'].pop()])) |\
				SELECTIONSTMT ~~ stack['s_node'].append(stack['selectionstmt_node'].pop()) |\
			    JUMPSTMT ~~ stack['s_node'].append(stack['jumpstmt_node'].pop())",
			"SELECTIONSTMT->if (COND) CSTMT ~~ stack['selectionstmt_node'].append(newNode('if',[stack['cond_node'].pop(),stack['cstmt_node'].pop()])) |\
							if (COND) CSTMT else CSTMT ~~ stack['selectionstmt_node'].append(newNode('if',[stack['cond_node'].pop(),stack['cstmt_node'].pop(-2),newLeafNode('else','else'),stack['cstmt_node'].pop()]))" ,
            "JUMPSTMT->continue; ~~ stack['jumpstmt_node'].append(newLeafNode('continue','continue')) |\
					   break; ~~ stack['jumpstmt_node'].append(newLeafNode('break','break')) |\
					   return E;~~ stack['jumpstmt_node'].append(newNode('return',[stack['e_node'].pop()])) |\
					   return; ~~ stack['jumpstmt_node'].append(newLeafNode('return','return'))",
			"DECL->TYPE VARLIST  ~~ stack['decl_node'].append(newNode('decl',[stack['type_node'].pop(),stack['varlist_node'].pop()])) |\
 				   TYPE ASSIGNEXPR ~~ stack['decl_node'].append(newNode('decl',[stack['type_node'].pop(),stack['assignexpr_node'].pop()]))" ,
		    "TYPE->int ~~ stack['type_node'].append(newLeafNode('type','int')) |\
 			       char ~~ stack['type_node'].append(newLeafNode('type','char')) |\
 			       float ~~ stack['type_node'].append(newLeafNode('type','float'))" ,
 			"VARLIST->id , VARLIST ~~ stack['varlist_node'].append(newNode('varlist',[newLeafNode('id',val.pop()),stack['varlist_node'].pop()])) |\
 			          id ; ~~ stack['varlist_node'].append(newLeafNode('id',val.pop()))" ,
 			"ASSIGNEXPR->id = E , ASSIGNEXPR ~~ stack['assignexpr_node'].append(newNode('assign_expr',[newNode('=',[newLeafNode('id',val.pop()),stack['e_node'].pop()]),stack['assignexpr_node'].pop()])) |\
						 id = E;  ~~ stack['assignexpr_node'].append(newNode('=',[newLeafNode('id',val.pop()),stack['e_node'].pop()]))" ,
			"E->E + T ~~ stack['e_node'].append(newNode('+',[stack['e_node'].pop(),stack['t_node'].pop()])) |\
				E - T ~~ stack['e_node'].append(newNode('-',[stack['e_node'].pop(),stack['t_node'].pop()])) |\
				T ~~ stack['e_node'].append(stack['t_node'].pop())" ,
			"T->T * F ~~ stack['t_node'].append(newNode('*',[stack['t_node'].pop(),stack['f_node'].pop()])) |\
				T / F ~~ stack['t_node'].append(newNode('/',[stack['t_node'].pop(),stack['f_node'].pop()])) |\
				F ~~ stack['t_node'].append(stack['f_node'].pop())" ,
			"F->id ~~ stack['f_node'].append(newLeafNode('id',val.pop())) |\
				num ~~ stack['f_node'].append(newLeafNode('num',val.pop())) |\
				(E) ~~ stack['f_node'].append(stack['e_node'].pop())" ,
            "COND->BE ~~ stack['cond_node'].append(stack['be_node'].pop())",
            "BE->BT ~~ stack['be_node'].append(stack['bt_node'].pop()) |\
                 BE || BT ~~ stack['be_node'].append(newNode('||',[stack['be_node'].pop(),stack['bt_node'].pop()]))",
            "BT->BF ~~ stack['bt_node'].append(stack['bf_node'].pop()) |\
                 BT && BF ~~ stack['bt_node'].append(newNode('&&',[stack['bt_node'].pop(),stack['bf_node'].pop()]))",
            "BF->(BE) ~~ stack['bf_node'].append(stack['be_node'].pop()) |\
                 ! BF ~~ stack['bf_node'].append(newNode('!',[stack['bf_node'].pop()])) |\
                 E rop E ~~ stack['bf_node'].append(newNode(val.pop(),[stack['e_node'].pop(-2),stack['e_node'].pop()]))"
		]

grammardict=dict()
regex=r'([A-Z_]+)|([a-z]+)|([\+\-\=\*\/]+)|([^ ])'
for production in grammar:
    #print(production)
    lhs,rhs=production.strip().split("->")
    rhs=rhs.strip().replace("||","[or]")
    rhs=rhs.split("|")
    grammardict[lhs]=[]
    for i in range(len(rhs)):
        rhs[i]=rhs[i].strip().replace("[or]","||")
        rhs[i]=rhs[i].strip().replace("\t","")
        fullRHS=rhs[i].split("~~")
        fullRHS[0]=fullRHS[0].strip()					#Production RHS
        fullRHS[-1]=fullRHS[-1].strip()					#Query if it exists
        fullRHS[0]=re.findall(regex,fullRHS[0])
        temp=[]
        for tup in fullRHS[0]:
            if(max(tup)!='epsilon'):
                temp.append(max(tup))
        finalrhs=dict()
        finalrhs['rhs']=temp
        if(len(fullRHS)>1):
        	finalrhs['query']=fullRHS[1]
        grammardict[lhs].append(finalrhs)

stack=dict()
for key,val in grammardict.items():
	query=key.lower()+'_node'
	query=query.strip()
	stack[query]=[]
	print(key)
	for d in val:
		print('production:',d['rhs'])
		if('query' in d):
			print('query:',d['query'])
	print()

#stack['cstmt_node'].append(1)


def newLeafNode(name,val):
	node=dict()
	node["name"]=name
	node["value"]=val
	node["leaf"]=True
	return node

def newNode(name,childList):
	node=dict()
	node["name"]=name
	node["leaf"]=False
	node["children"]=childList
	return node

#q="stack['func_defn_node'].append(newNode('main',[newLeafNode('type','int'),stack['cstmt_node'][-1]]))"
#eval(q)


def genAST(ptree):
    dfs(ptree['children'],ptree['Symbol'])

#print(stack)
print(parse_tree)
def dfs(nodes,name):
    productionlhs = name.upper()
    productionrhs = []
    val=[]
    for node in nodes:
        #print(i)
        if('Symbol' in node):
            dfs(node['children'],node['Symbol'])
        if('Symbol' in node):
            productionrhs.append(node['Symbol'].upper())
        else:
            productionrhs.append(node['type'])
            if(node['type']=='num'):
                val.append(node['num'])
            elif(node['type'] in ['id','rop']):
                val.append(node['buf'])

    for prod in grammardict[productionlhs]:
        print(prod['rhs'],productionrhs)
        if(prod['rhs']==productionrhs):
            print(prod['query'])
            eval(prod['query'])

tree=[]
genAST(parse_tree)
tr=Tree('main',[])
tr.pretty_print()
root=stack['program_node'][0]
def draw(root,tree):
	for i in root['children']:
		if(i is not None):
			if(root['name']=='if'):
				print(i['name'])
			if(i['leaf']):
				tree.append(Tree(i['name'],[i['value']]))
			else:
				tree.append(Tree(i['name'],[]))
		if(root['name']=='if'):
				tree.pretty_print()
	tr.pretty_print()
	j=0
	for i in root['children']:
		if(i is not None and not i['leaf']):
			draw(i,tree[j])
		j+=1
draw(root,tr)
