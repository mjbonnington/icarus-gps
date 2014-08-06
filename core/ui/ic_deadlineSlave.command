#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ic_deadlineSlave.command
#copyright	:Gramercy Park Studios

#This is custom deadline slave launcher sets the vray license up before launching the slave so slaves don't fail the job

/Applications/Autodesk/maya2014/vray/bin/setvrlservice -server=10.105.11.100;
/Applications/Thinkbox/Deadline6/DeadlineSlave.app/Contents/MacOS/DeadlineSlave;