"""
Main Fanuc TP Writer class for generating complete TP programs.
"""

from typing import List, Dict, Optional, Union, TextIO
from datetime import datetime
from .position import Position
from .commands import Command, MovementCommand, LogicCommand, IOCommand, WaitCommand, CallCommand, CommentCommand, LabelCommand, JumpCommand


class FanucTPWriter:
    """Main class for writing Fanuc TP programs."""
    
    def __init__(self, program_name: str = "MAIN"):
        """
        Initialize TP Writer.
        
        Args:
            program_name: Name of the TP program
        """
        self.program_name = program_name.upper()
        self.commands: List[Command] = []
        self.positions: Dict[int, Position] = {}
        self.registers: Dict[str, int] = {}
        self.current_line = 1
        
    def add_comment(self, text: str) -> 'FanucTPWriter':
        """Add a comment line."""
        self.commands.append(CommentCommand(text))
        self.current_line += 1
        return self
    
    def add_position(self, number: int, position: Position) -> 'FanucTPWriter':
        """Add a position definition."""
        self.positions[number] = position
        return self
    
    def move_joint(self, position: Union[int, Position], speed: Optional[Union[int, str]] = None, 
                   termination: str = "FINE", offset: Optional[str] = None) -> 'FanucTPWriter':
        """Add joint movement command."""
        self.commands.append(MovementCommand('J', position, speed, termination, offset))
        self.current_line += 1
        return self
    
    def move_linear(self, position: Union[int, Position], speed: Optional[Union[int, str]] = None, 
                    termination: str = "FINE", offset: Optional[str] = None) -> 'FanucTPWriter':
        """Add linear movement command."""
        self.commands.append(MovementCommand('L', position, speed, termination, offset))
        self.current_line += 1
        return self
    
    def move_circular(self, position: Union[int, Position], speed: Optional[Union[int, str]] = None, 
                      termination: str = "FINE", offset: Optional[str] = None) -> 'FanucTPWriter':
        """Add circular movement command."""
        self.commands.append(MovementCommand('C', position, speed, termination, offset))
        self.current_line += 1
        return self
    
    def if_condition(self, condition: str) -> 'FanucTPWriter':
        """Add IF statement."""
        self.commands.append(LogicCommand('IF', condition))
        self.current_line += 1
        return self
    
    def else_statement(self) -> 'FanucTPWriter':
        """Add ELSE statement."""
        self.commands.append(LogicCommand('ELSE'))
        self.current_line += 1
        return self
    
    def endif(self) -> 'FanucTPWriter':
        """Add ENDIF statement."""
        self.commands.append(LogicCommand('ENDIF'))
        self.current_line += 1
        return self
    
    def for_loop(self, register: int, start: int, end: int) -> 'FanucTPWriter':
        """Add FOR loop."""
        self.commands.append(LogicCommand('FOR', f'R[{register}]={start} TO {end}'))
        self.current_line += 1
        return self
    
    def endfor(self) -> 'FanucTPWriter':
        """Add ENDFOR statement."""
        self.commands.append(LogicCommand('ENDFOR'))
        self.current_line += 1
        return self
    
    def while_loop(self, condition: str) -> 'FanucTPWriter':
        """Add WHILE loop."""
        self.commands.append(LogicCommand('WHILE', condition))
        self.current_line += 1
        return self
    
    def endwhile(self) -> 'FanucTPWriter':
        """Add ENDWHILE statement."""
        self.commands.append(LogicCommand('ENDWHILE'))
        self.current_line += 1
        return self
    
    def set_digital_output(self, number: int, value: bool) -> 'FanucTPWriter':
        """Set digital output."""
        self.commands.append(IOCommand('DO', number, value))
        self.current_line += 1
        return self
    
    def set_robot_output(self, number: int, value: bool) -> 'FanucTPWriter':
        """Set robot output."""
        self.commands.append(IOCommand('RO', number, value))
        self.current_line += 1
        return self
    
    def set_group_output(self, number: int, value: int) -> 'FanucTPWriter':
        """Set group output."""
        self.commands.append(IOCommand('GO', number, value))
        self.current_line += 1
        return self
    
    def wait_for_condition(self, condition: str) -> 'FanucTPWriter':
        """Add wait for condition."""
        self.commands.append(WaitCommand('WAIT', condition=condition))
        self.current_line += 1
        return self
    
    def wait_time(self, seconds: float) -> 'FanucTPWriter':
        """Add wait for time."""
        self.commands.append(WaitCommand('WAIT', time=seconds))
        self.current_line += 1
        return self
    
    def pause(self) -> 'FanucTPWriter':
        """Add pause command."""
        self.commands.append(WaitCommand('PAUSE'))
        self.current_line += 1
        return self
    
    def stop(self) -> 'FanucTPWriter':
        """Add stop command."""
        self.commands.append(WaitCommand('STOP'))
        self.current_line += 1
        return self
    
    def call_program(self, program_name: str) -> 'FanucTPWriter':
        """Call another program."""
        self.commands.append(CallCommand('CALL', program_name))
        self.current_line += 1
        return self
    
    def run_program(self, program_name: str) -> 'FanucTPWriter':
        """Run another program."""
        self.commands.append(CallCommand('RUN', program_name))
        self.current_line += 1
        return self
    
    def abort(self) -> 'FanucTPWriter':
        """Add abort command."""
        self.commands.append(CallCommand('ABORT'))
        self.current_line += 1
        return self
    
    def label(self, number: int) -> 'FanucTPWriter':
        """Add label."""
        self.commands.append(LabelCommand(number))
        self.current_line += 1
        return self
    
    def jump_to_label(self, number: int, condition: Optional[str] = None) -> 'FanucTPWriter':
        """Add jump to label."""
        self.commands.append(JumpCommand(number, condition))
        self.current_line += 1
        return self
    
    def generate_tp_program(self) -> str:
        """Generate the complete TP program as a string."""
        lines = []
        
        # Program header
        lines.append(f"/PROG  {self.program_name}")
        lines.append(f"/ATTR")
        lines.append(f"OWNER\t\t= MNEDITOR;")
        lines.append(f"COMMENT\t\t= \"Generated by PY-to-Franuc-TP\";")
        lines.append(f"PROG_SIZE\t= {len(self.commands) + 10};")
        lines.append(f"CREATE\t\t= DATE {datetime.now().strftime('%y-%m-%d')}  TIME {datetime.now().strftime('%H:%M:%S')};")
        lines.append(f"MODIFIED\t= DATE {datetime.now().strftime('%y-%m-%d')}  TIME {datetime.now().strftime('%H:%M:%S')};")
        lines.append(f"FILE_NAME\t= {self.program_name};")
        lines.append(f"VERSION\t\t= 0;")
        lines.append(f"LINE_COUNT\t= {len(self.commands) + 2};")
        lines.append("/MN")
        
        # Add positions
        if self.positions:
            lines.append("   : ! Position Definitions")
            for pos_num, position in sorted(self.positions.items()):
                if position.joints:
                    lines.append(f"   : {position.to_joint_string(pos_num)}")
                else:
                    lines.append(f"   : {position.to_cartesian_string(pos_num)}")
            lines.append("   :")
        
        # Add program commands
        line_num = 1
        for command in self.commands:
            lines.append(f"   {line_num}: {command.to_tp_string()}")
            line_num += 1
        
        # Program footer
        lines.append(f"   {line_num}: END ;")
        lines.append("/POS")
        lines.append("/END")
        
        return '\n'.join(lines)
    
    def save_to_file(self, filename: str) -> None:
        """Save the TP program to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_tp_program())
    
    def clear(self) -> 'FanucTPWriter':
        """Clear all commands and positions."""
        self.commands.clear()
        self.positions.clear()
        self.current_line = 1
        return self