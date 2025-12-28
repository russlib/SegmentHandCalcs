import mmap
import struct

class SimInfo:
    def __init__(self):
        self._physics_map = mmap.mmap(0, 712, "Local\\acpmf_physics")
    
    def close(self):
        self._physics_map.close()

    @property
    def physics(self):
        # Unpack the specific data points from the C++ struct
        # Structure format based on AC Shared Memory documentation
        data = self._physics_map.read(712)
        self._physics_map.seek(0)
        
        # We parse the binary data to get your exact numbers
        # P = Packet Index, f = float, I = Int
        # 0: PacketID, 1: Gas, 2: Brake, 3: Fuel, 4: Gear, 5: RPM, 6: SteerAngle
        # 7: SpeedKmh, 8-10: Velocity Vector, 11-13: AccG, 14-16: WheelSlip...
        # ... 26-29: WheelLoad ... 50: EngineTorque ... 52: Pitch, 53: Roll
        
        fmt = "I f f f i f f f 3f 3f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f f f"
        # Note: This is a simplified unpack for the standard physics header
        # We need to handle the offsets manually for safety or use the full struct
        
        # Let's do direct offset reading for maximum reliability without a huge library
        return PhysicsData(data)

class PhysicsData:
    def __init__(self, bytes_data):
        # 1. Speed (Offset 28, float) -> Convert Kmh to m/s
        self.speed_ms = struct.unpack_from('f', bytes_data, 28)[0] / 3.6
        
        # 2. RPM (Offset 20, float)
        self.rpms = struct.unpack_from('f', bytes_data, 20)[0]
        
        # 3. G-Forces (Offset 44, 3 floats: X, Y, Z)
        self.accG = struct.unpack_from('3f', bytes_data, 44)
        
        # 4. Wheel Loads (Offset 108, 4 floats: FL, FR, RL, RR)
        self.wheel_load = struct.unpack_from('4f', bytes_data, 108)
        
        # 5. Engine Torque (Offset 248, float)
        self.engine_torque = struct.unpack_from('f', bytes_data, 248)[0]
        
        # 6. Tilt: Pitch & Roll (Offsets 256 and 260)
        self.pitch = struct.unpack_from('f', bytes_data, 256)[0]
        self.roll = struct.unpack_from('f', bytes_data, 260)[0]

        # 7. Center of Gravity Height (Offset 264)
        self.cg_height = struct.unpack_from('f', bytes_data, 264)[0]