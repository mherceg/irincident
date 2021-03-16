#!/usr/bin/env python3
import irsdk
from time import sleep

CLOSENESS_THRESHOLD_PERCENTAGE = 4
INCIDENT_DuRATION = 10

def init():
	ir = None
	return ir

def set_liveries(ir, involved_idx):
	pass
	#return liveries

def restore_liveries(ir, past_liveries):
	pass

def record_next_incident(ir):
	#Seek incident
	# sleep(10)
	inc_idx = ir['PlayerCarIdx']
	all_positions = ir['CarIdxLapDistPct']
	inc_position = ir[inc_idx]
	involved_idx = [inc_idx]
	for i,p in enumerate(all_positions):
		if abs(p - inc_position) < CLOSENESS_THRESHOLD_PERCENTAGE:
			involved_idx.append((p, i))
	involved_idx = map(lambda x: x[1], sorted(involved_idx))
	liveries_info = set_liveries(ir, involved_idx)
	sleep(10) 
	#Set cam, car combination (Far chase, Rear chase, Onboards, Chopper)
	#Cam on last, far chase
	#Cam on first, rear chase
	for i in involved_idx:
		#Onboard
	restore_liveries(ir, past_liveries)
	#return involved cars
	pass

def race_done(ir):
	pass

def main():
	ir = init()
	#seek_race_start(ir)
	while not race_done(ir):
		involved = record_next_incident(ir)
	#Create title picture
	#Log involved + colours

if __name__ == '__main__':
	main()