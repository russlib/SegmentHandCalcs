import mmap
import time
import ctypes
import csv
import math

# --- ENGINEERING CONSTANTS (EDIT THESE FOR YOUR CAR) ---
CAR_MASS_KG = 1200.0      # Total mass (Car + Driver)
WHEEL_RADIUS_M = 0.33     # Radius of the rear tires
Cd = 0.30                 # Drag Coefficient (Estimated)
FRONTAL_AREA = 2.0        # m^2
AIR_DENSITY = 1.225       # kg/m^3

# --- 2. MEMORY STRUCTURE ---
class SPageFilePhysics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("gas", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("gear", ctypes.c_int),
        ("rpms", ctypes.c_int),
        ("steerAngle", ctypes.c_float),
        ("speedKmh", ctypes.c_float),
        ("velocity", ctypes.c_float * 3),
        ("accG", ctypes.c_float * 3),
        ("wheelSlip", ctypes.c_float * 4),
        ("wheelLoad", ctypes.c_float * 4),
        ("wheelsPressure", ctypes.c_float * 4),
        ("wheelAngularSpeed", ctypes.c_float * 4),
        ("tyreWear", ctypes.c_float * 4),
        ("tyreDirtyLevel", ctypes.c_float * 4),
        ("tyreCoreTemp", ctypes.c_float * 4),
        ("camberRAD", ctypes.c_float * 4),
        ("suspensionTravel", ctypes.c_float * 4),
        ("drs", ctypes.c_float),
        ("tc", ctypes.c_float),
        ("heading", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("cgHeight", ctypes.c_float),
        ("carDamage", ctypes.c_float * 5),
        ("numberOfTyresOut", ctypes.c_int),
        ("pitLimiterOn", ctypes.c_int),
        ("abs", ctypes.c_float),
        ("kersCharge", ctypes.c_float),
        ("kersInput", ctypes.c_float),
        ("autoShifterOn", ctypes.c_int),
        ("rideHeight", ctypes.c_float * 2),
        ("turboBoost", ctypes.c_float),
    ]

def main():
    print("Connecting to Physics Engine...")
    try:
        shm = mmap.mmap(0, ctypes.sizeof(SPageFilePhysics), "Local\\acpmf_physics")
    except FileNotFoundError:
        print("Error: Assetto Corsa not found. Go on track first!")
        return

    filename = f"telemetry_wheel_torque_{int(time.time())}.csv"
    print(f"Logging to {filename}...")

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Time", "Speed_MS", "RPM", "Long_Accel_G", 
            "Drag_Force_N", "Net_Force_N", "Total_Tractive_Force_N", 
            "Est_Wheel_Torque_Nm"
        ])

        start_t = time.time()
        
        try:
            while True:
                shm.seek(0)
                data = SPageFilePhysics.from_buffer_copy(shm.read(ctypes.sizeof(SPageFilePhysics)))
                
                if data.rpms < 100:
                    time.sleep(0.1)
                    continue

                # --- ENGINEERING MATH ---
                
                # 1. Variables
                speed_ms = data.speedKmh / 3.6
                long_acc_g = data.accG[2] # Longitudinal G (Forward/Back)
                long_acc_ms2 = long_acc_g * 9.81
                
                # 2. Calculate Aero Drag Force (F_aero = 0.5 * p * v^2 * Cd * A)
                # We add this because the engine has to OVERCOME drag to accelerate
                f_aero = 0.5 * AIR_DENSITY * (speed_ms ** 2) * Cd * FRONTAL_AREA
                
                # 3. Calculate Net Force (F = ma)
                # This is the "Leftover" force that actually accelerated the mass
                f_net = CAR_MASS_KG * long_acc_ms2
                
                # 4. Total Tractive Force (The total push from the tires)
                # If you are cruising at constant speed, f_net is 0, but f_tractive = f_aero
                f_tractive = f_net + f_aero
                
                # 5. Wheel Torque (Total across driven wheels)
                # Torque = Force * Radius
                wheel_torque = f_tractive * WHEEL_RADIUS_M
                
                # Filter out negative torque (braking) if you only want engine power
                if data.gas == 0 and wheel_torque < 0:
                     # This is braking torque
                     pass 

                writer.writerow([
                    round(time.time() - start_t, 3),
                    round(speed_ms, 2),
                    data.rpms,
                    round(long_acc_g, 3),
                    round(f_aero, 1),
                    round(f_net, 1),
                    round(f_tractive, 1),
                    round(wheel_torque, 1)
                ])
                time.sleep(0.02) # 50Hz

        except KeyboardInterrupt:
            print("Stopped.")
            shm.close()

if __name__ == "__main__":
    main()