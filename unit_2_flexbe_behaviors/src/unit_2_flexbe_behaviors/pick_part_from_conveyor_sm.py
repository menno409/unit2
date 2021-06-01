#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_conveyorSM(Behavior):
	'''
	pick's a part form athe conveyor
	'''


	def __init__(self):
		super(pick_part_from_conveyorSM, self).__init__()
		self.name = 'pick_part_from_conveyor'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:868 y:333, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['robot_namespace'], output_keys=['part'])
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.world = 'world'
		_state_machine.userdata.camera_frame = 'logical_camera_5_frame'
		_state_machine.userdata.topic_camera = '/ariac/logical_camera_5'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = 'ariac/arm2'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.offset = 0.035
		_state_machine.userdata.rotation = 3.145
		_state_machine.userdata.gripper2 = '/ariac/arm2/gripper/control'
		_state_machine.userdata.config_name_home = 'home'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.part = "gasket_part"
		_state_machine.userdata.part2 = "piston_rod_part"
		_state_machine.userdata.part3 = "gear_part"
		_state_machine.userdata.config_pregrasp = 'Conveyor2PreGrasp'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:142 y:48
			OperatableStateMachine.add('detect part',
										DetectPartCameraAriacState(time_out=100),
										transitions={'continue': 'Compute pick', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'world', 'camera_topic': 'topic_camera', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:369 y:36
			OperatableStateMachine.add('Compute pick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'Activae gripper', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:827 y:61
			OperatableStateMachine.add('Move Pre Grasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move R2 to pick', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_pregrasp', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_pregrasp', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1101 y:79
			OperatableStateMachine.add('Move R2 to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:604 y:52
			OperatableStateMachine.add('Activae gripper',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'Move Pre Grasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper2'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
