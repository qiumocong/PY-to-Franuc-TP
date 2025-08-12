"""
Position handling for Fanuc robot coordinates.
"""

from typing import Dict, List, Optional, Union


class Position:
    """Represents a robot position in Fanuc TP format."""
    
    def __init__(self, 
                 x: float = 0.0, 
                 y: float = 0.0, 
                 z: float = 0.0,
                 w: float = 0.0, 
                 p: float = 0.0, 
                 r: float = 0.0,
                 config: Optional[str] = None,
                 joints: Optional[List[float]] = None):
        """
        Initialize a robot position.
        
        Args:
            x, y, z: Cartesian coordinates (mm)
            w, p, r: Orientation (degrees) - Yaw, Pitch, Roll
            config: Robot configuration string (e.g., 'N U T, 0, 0, 0')
            joints: Joint angles for joint positions [J1, J2, J3, J4, J5, J6]
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.p = p
        self.r = r
        self.config = config or 'N U T, 0, 0, 0'
        self.joints = joints
        
    def to_cartesian_string(self, position_number: int) -> str:
        """Convert to Fanuc TP cartesian position format."""
        return (f"P[{position_number}]{{\n"
                f"   GP1:\n"
                f"    UF : 0, UT : 1,    CONFIG : '{self.config}',\n"
                f"    X = {self.x:8.3f} mm, Y = {self.y:8.3f} mm, Z = {self.z:8.3f} mm,\n"
                f"    W = {self.w:8.3f} deg, P = {self.p:8.3f} deg, R = {self.r:8.3f} deg\n"
                f"}};")
    
    def to_joint_string(self, position_number: int) -> str:
        """Convert to Fanuc TP joint position format."""
        if not self.joints or len(self.joints) != 6:
            raise ValueError("Joint position requires 6 joint angles")
        
        return (f"P[{position_number}]{{\n"
                f"   GP1:\n"
                f"    UF : 0, UT : 1,\n"
                f"    J1 = {self.joints[0]:8.3f} deg, J2 = {self.joints[1]:8.3f} deg, J3 = {self.joints[2]:8.3f} deg,\n"
                f"    J4 = {self.joints[3]:8.3f} deg, J5 = {self.joints[4]:8.3f} deg, J6 = {self.joints[5]:8.3f} deg\n"
                f"}};")
    
    @classmethod
    def from_xyz(cls, x: float, y: float, z: float, w: float = 0.0, p: float = 0.0, r: float = 0.0) -> 'Position':
        """Create position from XYZ coordinates."""
        return cls(x=x, y=y, z=z, w=w, p=p, r=r)
    
    @classmethod
    def from_joints(cls, j1: float, j2: float, j3: float, j4: float, j5: float, j6: float) -> 'Position':
        """Create position from joint angles."""
        return cls(joints=[j1, j2, j3, j4, j5, j6])