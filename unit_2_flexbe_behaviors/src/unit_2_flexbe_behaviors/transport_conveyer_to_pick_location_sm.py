#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_break_beam_state import DetectBreakBeamState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 27 2021
@author: Menno Spriensma
'''
class transport_conveyer_to_pick_locationSM(Behavior):
	'''
	Deze toestandsmachine zet de transportband aan totdat er een part aan
komt op de plaats waar je het wilt oppakken met een robot.
	'''


	def __init__(self):
		super(transport_conveyer_to_pick_locationSM, self).__init__()
		self.name = 'transport_conveyer_to_pick_location'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1026 y:79, x:21 y:613
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.speedstart = 100
		_state_machine.userdata.speedstop = 0
		_state_machine.userdata.config_name_home = 'AGV2PreDrop'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = 'ariac/arm2'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.topic_break_beam2 = '/ariac/break_beam_2_change'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:46 y:50
			OperatableStateMachine.add('start assignment',
										StartAssignment(),
										transitions={'continue': 'Move R2 Home'},
										autonomy={'continue': Autonomy.Off})

			# x:168 y:50
			OperatableStateMachine.add('Move R2 Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Start conveyer', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_home', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_home', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:349 y:44
			OperatableStateMachine.add('Start conveyer',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'Detectpart', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'speedstart'})

			# x:764 y:62
			OperatableStateMachine.add('Stop conveyer',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'speedstop'})

			# x:560 y:43
			OperatableStateMachine.add('Detectpart',
										DetectBreakBeamState(),
										transitions={'continue': 'Stop conveyer', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'topic': 'topic_break_beam2', 'object_detected': 'object_detected'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
