"""
Command classes for Fanuc TP programming.
"""

from abc import ABC, abstractmethod
from typing import Union, List, Optional
from .position import Position


class Command(ABC):
    """Base class for all Fanuc TP commands."""
    
    @abstractmethod
    def to_tp_string(self) -> str:
        """Convert command to Fanuc TP string format."""
        pass


class MovementCommand(Command):
    """Represents robot movement commands (J, L, C)."""
    
    def __init__(self, 
                 move_type: str, 
                 position: Union[int, Position], 
                 speed: Optional[Union[int, str]] = None,
                 termination: str = "FINE",
                 offset: Optional[str] = None):
        """
        Initialize movement command.
        
        Args:
            move_type: Type of movement ('J', 'L', 'C')
            position: Position number or Position object
            speed: Speed setting (1-100% or R[x])
            termination: Motion termination ('FINE' or 'CNT100', etc.)
            offset: Position offset (e.g., 'OFFSET,PR[1]')
        """
        self.move_type = move_type.upper()
        self.position = position
        self.speed = speed or 100
        self.termination = termination
        self.offset = offset
        
        if self.move_type not in ['J', 'L', 'C']:
            raise ValueError("Move type must be 'J', 'L', or 'C'")
    
    def to_tp_string(self) -> str:
        """Convert to TP movement command string."""
        if isinstance(self.position, Position):
            pos_ref = "P[pos]"  # Position would need to be defined separately
        else:
            pos_ref = f"P[{self.position}]"
        
        speed_str = f"{self.speed}%" if isinstance(self.speed, int) else str(self.speed)
        
        parts = [f"{self.move_type}", pos_ref, speed_str, self.termination]
        
        if self.offset:
            parts.append(self.offset)
        
        return f"{self.move_type} {pos_ref} {speed_str} {self.termination}" + (f" {self.offset}" if self.offset else "") + " ;"


class LogicCommand(Command):
    """Represents logic control commands."""
    
    def __init__(self, command_type: str, condition: Optional[str] = None, value: Optional[Union[int, str]] = None):
        """
        Initialize logic command.
        
        Args:
            command_type: Type of logic command ('IF', 'ELSE', 'ENDIF', 'FOR', 'ENDFOR', 'WHILE', 'ENDWHILE')
            condition: Condition for IF/WHILE commands
            value: Value for FOR loops
        """
        self.command_type = command_type.upper()
        self.condition = condition
        self.value = value
    
    def to_tp_string(self) -> str:
        """Convert to TP logic command string."""
        if self.command_type in ['IF', 'WHILE']:
            if not self.condition:
                raise ValueError(f"{self.command_type} command requires a condition")
            return f"{self.command_type} {self.condition} THEN"
        elif self.command_type == 'FOR':
            if not self.value:
                raise ValueError("FOR command requires a value")
            return f"FOR R[{self.value}]=1 TO {self.value}"
        elif self.command_type in ['ELSE', 'ENDIF', 'ENDFOR', 'ENDWHILE']:
            return f"{self.command_type}"
        else:
            raise ValueError(f"Unknown logic command type: {self.command_type}")


class IOCommand(Command):
    """Represents I/O commands."""
    
    def __init__(self, io_type: str, number: int, value: Optional[Union[bool, int]] = None, action: str = "SET"):
        """
        Initialize I/O command.
        
        Args:
            io_type: Type of I/O ('DO', 'DI', 'RO', 'RI', 'GO', 'GI')
            number: I/O number
            value: Value to set (for output commands)
            action: Action type ('SET', 'RESET', 'PULSE')
        """
        self.io_type = io_type.upper()
        self.number = number
        self.value = value
        self.action = action.upper()
    
    def to_tp_string(self) -> str:
        """Convert to TP I/O command string."""
        if self.io_type in ['DO', 'RO']:
            if self.value is None:
                raise ValueError(f"{self.io_type} command requires a value")
            
            if isinstance(self.value, bool):
                value_str = "ON" if self.value else "OFF"
            else:
                value_str = str(self.value)
            
            return f"{self.io_type}[{self.number}]={value_str} ;"
        
        elif self.io_type in ['GO']:
            if self.value is None:
                raise ValueError(f"{self.io_type} command requires a value")
            return f"{self.io_type}[{self.number}]={self.value} ;"
        
        else:  # Input commands
            return f"! Read {self.io_type}[{self.number}]"


class WaitCommand(Command):
    """Represents wait and delay commands."""
    
    def __init__(self, wait_type: str, condition: Optional[str] = None, time: Optional[float] = None):
        """
        Initialize wait command.
        
        Args:
            wait_type: Type of wait ('WAIT', 'PAUSE', 'STOP')
            condition: Wait condition (e.g., 'DI[1]=ON')
            time: Wait time in seconds
        """
        self.wait_type = wait_type.upper()
        self.condition = condition
        self.time = time
    
    def to_tp_string(self) -> str:
        """Convert to TP wait command string."""
        if self.wait_type == 'WAIT':
            if self.condition:
                return f"WAIT FOR {self.condition} ;"
            elif self.time:
                return f"WAIT {self.time:.1f}(sec) ;"
            else:
                raise ValueError("WAIT command requires either condition or time")
        
        elif self.wait_type == 'PAUSE':
            return "PAUSE ;"
        
        elif self.wait_type == 'STOP':
            return "STOP ;"
        
        else:
            raise ValueError(f"Unknown wait command type: {self.wait_type}")


class CallCommand(Command):
    """Represents program call commands."""
    
    def __init__(self, command_type: str, program_name: Optional[str] = None):
        """
        Initialize call command.
        
        Args:
            command_type: Type of call ('CALL', 'RUN', 'ABORT')
            program_name: Name of program to call/run
        """
        self.command_type = command_type.upper()
        self.program_name = program_name
    
    def to_tp_string(self) -> str:
        """Convert to TP call command string."""
        if self.command_type in ['CALL', 'RUN']:
            if not self.program_name:
                raise ValueError(f"{self.command_type} command requires a program name")
            return f"{self.command_type} {self.program_name} ;"
        
        elif self.command_type == 'ABORT':
            return "ABORT ;"
        
        else:
            raise ValueError(f"Unknown call command type: {self.command_type}")


class CommentCommand(Command):
    """Represents comment lines."""
    
    def __init__(self, text: str):
        """Initialize comment command."""
        self.text = text
    
    def to_tp_string(self) -> str:
        """Convert to TP comment string."""
        return f"! {self.text}"


class LabelCommand(Command):
    """Represents label commands for program flow control."""
    
    def __init__(self, label_number: int):
        """Initialize label command."""
        self.label_number = label_number
    
    def to_tp_string(self) -> str:
        """Convert to TP label string."""
        return f"LBL[{self.label_number}] ;"


class JumpCommand(Command):
    """Represents jump commands."""
    
    def __init__(self, label_number: int, condition: Optional[str] = None):
        """
        Initialize jump command.
        
        Args:
            label_number: Label number to jump to
            condition: Optional condition for conditional jump
        """
        self.label_number = label_number
        self.condition = condition
    
    def to_tp_string(self) -> str:
        """Convert to TP jump command string."""
        if self.condition:
            return f"JMP LBL[{self.label_number}] IF {self.condition} ;"
        else:
            return f"JMP LBL[{self.label_number}] ;"