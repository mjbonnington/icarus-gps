# GPS Keyframe Flip
# v0.1
#
# Michael Bonnington 2017
# Gramercy Park Studios

import maya.cmds as mc

def flip():
	keys = mc.keyframe(q=1)
	pivot_key = (min(keys)+max(keys)) / 2.0

	mc.scaleKey(iub=False, ts=-1, tp=pivot_key, animation='keys')
