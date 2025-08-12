"""
Example usage of PY-to-Franuc-TP library.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fanuc_tp import FanucTPWriter, Position


def simple_pick_place_example():
    """Create a simple pick and place program."""
    # Create TP writer
    tp = FanucTPWriter("PICK_PLACE")
    
    # Define positions
    home_pos = Position.from_joints(0, 0, 0, 0, 0, 0)
    pick_approach = Position.from_xyz(100, 200, 300, 0, 180, 0)
    pick_pos = Position.from_xyz(100, 200, 250, 0, 180, 0)
    place_approach = Position.from_xyz(300, 200, 300, 0, 180, 0)
    place_pos = Position.from_xyz(300, 200, 250, 0, 180, 0)
    
    # Add positions to program
    tp.add_position(1, home_pos)
    tp.add_position(2, pick_approach)
    tp.add_position(3, pick_pos)
    tp.add_position(4, place_approach)
    tp.add_position(5, place_pos)
    
    # Create program
    tp.add_comment("Simple Pick and Place Program") \
      .add_comment("Move to home position") \
      .move_joint(1, 50) \
      .add_comment("Move to pick approach") \
      .move_linear(2, 100) \
      .add_comment("Move to pick position") \
      .move_linear(3, 25, "FINE") \
      .add_comment("Close gripper") \
      .set_digital_output(1, True) \
      .wait_time(0.5) \
      .add_comment("Move to pick approach") \
      .move_linear(2, 50) \
      .add_comment("Move to place approach") \
      .move_joint(4, 100) \
      .add_comment("Move to place position") \
      .move_linear(5, 25, "FINE") \
      .add_comment("Open gripper") \
      .set_digital_output(1, False) \
      .wait_time(0.5) \
      .add_comment("Move to place approach") \
      .move_linear(4, 50) \
      .add_comment("Return to home") \
      .move_joint(1, 100)
    
    return tp


def advanced_program_example():
    """Create an advanced program with logic and I/O."""
    tp = FanucTPWriter("ADVANCED")
    
    # Define positions
    home_pos = Position.from_joints(0, 0, 0, 0, 0, 0)
    work_pos = Position.from_xyz(200, 300, 400, 0, 180, 0)
    
    tp.add_position(1, home_pos)
    tp.add_position(2, work_pos)
    
    # Create advanced program with logic
    tp.add_comment("Advanced Program with Logic and I/O") \
      .add_comment("Initialize") \
      .move_joint(1, 50) \
      .set_digital_output(1, False) \
      .set_digital_output(2, False) \
      .add_comment("Main loop") \
      .label(1) \
      .add_comment("Check if start signal is ON") \
      .wait_for_condition("DI[1]=ON") \
      .add_comment("Move to work position") \
      .move_linear(2, 100) \
      .add_comment("Check part present sensor") \
      .if_condition("DI[2]=ON") \
      .add_comment("Part is present - process it") \
      .set_digital_output(1, True) \
      .wait_time(2.0) \
      .set_digital_output(1, False) \
      .set_digital_output(2, True) \
      .else_statement() \
      .add_comment("No part - set alarm") \
      .set_digital_output(3, True) \
      .pause() \
      .endif() \
      .add_comment("Return home") \
      .move_joint(1, 75) \
      .add_comment("Wait for cycle complete") \
      .wait_for_condition("DI[1]=OFF") \
      .set_digital_output(2, False) \
      .add_comment("Jump back to start") \
      .jump_to_label(1)
    
    return tp


def save_examples():
    """Save example programs to files."""
    # Create examples directory if it doesn't exist
    examples_dir = os.path.dirname(__file__)
    
    # Generate simple pick and place
    simple_tp = simple_pick_place_example()
    simple_tp.save_to_file(os.path.join(examples_dir, "pick_place.ls"))
    print("Generated: pick_place.ls")
    
    # Generate advanced program
    advanced_tp = advanced_program_example()
    advanced_tp.save_to_file(os.path.join(examples_dir, "advanced.ls"))
    print("Generated: advanced.ls")
    
    # Print program contents to console
    print("\n" + "="*50)
    print("SIMPLE PICK AND PLACE PROGRAM:")
    print("="*50)
    print(simple_tp.generate_tp_program())
    
    print("\n" + "="*50)
    print("ADVANCED PROGRAM:")
    print("="*50)
    print(advanced_tp.generate_tp_program())


if __name__ == "__main__":
    save_examples()