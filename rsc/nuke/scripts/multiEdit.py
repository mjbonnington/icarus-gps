import nuke
import types



def multiEdit():

 sel = nuke.selectedNodes()
 counter = 0

 if len(sel) == 0:
    nuke.message("please select a node")
    return

 p = nuke.Panel("multi edit:")

 p.addSingleLineInput("field: ","enter field")
 p.addEnumerationPulldown("new value is","value expression")
 p.addSingleLineInput("new value: ","enter new value")
 p.addButton("cancel")    
 p.addButton("edit")

 result = p.show()

 if result == 0 :
    return

 if result == 1:

    field = p.value("field: ")
    newVal = p.value("new value: ")
    isExpr = (p.value("new value is") == "expression")

    if isExpr:
	     
	     for node in sel:
		     
		     try:
			node.knob(field).setExpression(newVal)
			     
		     except:
			
			nuke.message("error while setting expression")
			          						
    else:
	     			
			     
	for i in sel :
		
		try:
			newValType = type(i.knob(field).value())		 
	
			try :
		
				if newValType == float:	
						
					i.knob(field).setValue(float(newVal))
							
				if newValType == int:	
						
					i.knob(field).setValue(int(newVal))
					
				if newValType == unicode:
							
					i.knob(field).setValue(unicode(newVal))
			
				if newValType == tuple:	
						
					i.knob(field).setValue(float(newVal))
							
				if newValType == str:
					
					i.knob(field).setValue(str(newVal))
		
		
			except :
				nuke.message('sorry, something went wrong')
				return
	
		except:
			pass