import nuke

t=nuke.menu("Nodes")
u=t.addMenu("Pixelfudger", icon="pxf_ICmenu.png")
 
t.addCommand( "Pixelfudger/PxF_Bandpass", "nuke.createNode('PxF_Bandpass')", icon="pxf_bandpass.png" ) 
t.addCommand( "Pixelfudger/PxF_ChromaBlur", "nuke.createNode('PxF_ChromaBlur')", icon="pxf_chromablur.png") 
t.addCommand( "Pixelfudger/PxF_Distort", "nuke.createNode('PxF_Distort')", icon="pxf_distort.png") 
t.addCommand( "Pixelfudger/PxF_Erode", "nuke.createNode('PxF_Erode')", icon="pxf_erode.png")
t.addCommand( "Pixelfudger/PxF_Filler", "nuke.createNode('PxF_Filler')", icon="pxf_filler.png") 
t.addCommand( "Pixelfudger/PxF_HueSat", "nuke.createNode('PxF_HueSat')", icon="pxf_huesat.png")  
t.addCommand( "Pixelfudger/PxF_KillSpill", "nuke.createNode('PxF_KillSpill')", icon="pxf_killspill.png") 
t.addCommand( "Pixelfudger/PxF_ScreenClean", "nuke.createNode('PxF_ScreenClean')", icon="pxf_screenclean.png") 

