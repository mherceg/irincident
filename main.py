#!/usr/bin/env python3
import irsdk
from time import sleep
import pyautogui

CLOSENESS_THRESHOLD_PERCENTAGE = 1
INCIDENT_DURATION = 10
RECORDING = True
INFO_DURATION = 2

LIVERIES = []

class camera:
	far_chase = 19
	onboard = 9
	rear_chase = 20
	chopper = 16

def init():
	ir = irsdk.IRSDK()
	ir.startup()
	print('Set iracing replay as the active window.')
	print('Turn on the iracing UI')
	print('Make sure OBS is running and ready')
	return ir

def change_livery(d, l):
	pass

def set_liveries(ir, involved_idx):
	liveries = LIVERIES
	drivers = []
	for cidx in involved_idx:
		for d in ir['DriverInfo']['Drivers']:
			if d['CarIdx'] == cidx:
				drivers.append(d)
	if len(drivers) > len(liveries):
		print('Missing liveries', len(drivers), len(liveries))
	for d, l in zip(drivers, liveries): 
		change_livery(d, l)
	return drivers

def restore_liveries(ir, past_liveries):
	pass

def recording():
	with pyautogui.hold('alt'):
		pyautogui.press('tab')
	sleep(0.5)
	if RECORDING:
		with pyautogui.hold('alt'):
			pyautogui.press('f9')
	sleep(0.5)
	with pyautogui.hold('alt'):
		pyautogui.press('tab')

def toggle_ui():
	pyautogui.press('space')

def rewind(ir, frame):
	ir.replay_set_play_position(irsdk.RpyPosMode.current, frame - ir['ReplayFrameNum'])

def start_replay(ir):
	ir.replay_set_play_speed(1)

def stop_replay(ir):
	ir.replay_set_play_speed(0)

def get_car_number(ir, idx):
	for d in ir['DriverInfo']['Drivers']:
		if d['CarIdx'] == idx:
			return d['CarNumber']

def record_camera(ir, idx, cam):
	print(f'Recording {idx} {cam}')
	ir.cam_switch_num(get_car_number(ir, idx), cam)
	sleep(0.5)
	toggle_ui()
	sleep(INFO_DURATION)
	toggle_ui()
	start_replay(ir)
	sleep(INCIDENT_DURATION)
	stop_replay(ir)

def record_next_incident(ir):
	ir.replay_search(irsdk.RpySrchMode.next_incident)
	sleep(1)
	inc_idx = ir['CamCarIdx']
	all_positions = ir['CarIdxLapDistPct']
	inc_position = ir['CarIdxLapDistPct'][inc_idx]
	frame = ir['ReplayFrameNum']
	involved_idx = []
	for i,p in enumerate(all_positions):
		if abs(p - inc_position)*100 < CLOSENESS_THRESHOLD_PERCENTAGE:
			involved_idx.append((p, i))
	if len(involved_idx) < 2:
		return None
	involved_idx = list(map(lambda x: x[1], sorted(involved_idx, reverse=True)))
	liveries_info = set_liveries(ir, involved_idx)
	print('\n'.join([i['UserName'] for i in liveries_info]))
	recording()
	record_camera(ir, inc_idx, camera.far_chase)
	rewind(ir, frame)
	record_camera(ir, inc_idx, camera.chopper)
	rewind(ir, frame)
	if involved_idx[-1] != inc_idx:
		record_camera(ir, involved_idx[-1], camera.far_chase)
		rewind(ir, frame)
	record_camera(ir, involved_idx[0], camera.rear_chase)
	rewind(ir, frame)
	for i in involved_idx:
		record_camera(ir, i, camera.onboard)
		rewind(ir, frame)
	recording()
	restore_liveries(ir, liveries_info)
	#return involved cars
	pass

def race_done(ir):
	return ir['SessionState'] == irsdk.SessionState.cool_down

def main():
	ir = init()
	sleep(4)
	ir.replay_search_session_time(0,0)
	sleep(2)
	ir.replay_search_session_time(2,0)
	sleep(4)
	stop_replay(ir)
	toggle_ui()
	while not race_done(ir):
		involved = record_next_incident(ir)
		sleep(5)
	#Create title picture
	#Log involved + colours

if __name__ == '__main__':
	main()