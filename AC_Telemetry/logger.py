import time
import csv
from sim_info import SimInfo

def main():
    print("Connecting to Assetto Corsa...")
    try:
        sim = SimInfo()
    except FileNotFoundError:
        print("Error: Assetto Corsa is not running! Start the game first.")
        return

    print("Logging started! Press Ctrl+C to stop.")
    
    # Create the CSV with your EXACT columns
    filename = f"telemetry_{int(time.time())}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # YOUR REQUESTED HEADERS
        headers = [
            "Time",
            "Lap_Number",           # For separation of laps
            "Engine_RPM",           # For Power Calcs
            "Engine_Torque_Nm",     # For Power & Traction
            "Speed_MS",             # For Speed Analysis
            "Lat_Accel_G",          # For Tire Efficiency
            "Long_Accel_G",         # Tire Efficiency & Balance
            "Pitch_Rad",            # Analysis of Tilt (Forward/Back)
            "Roll_Rad",             # Analysis of Tilt (Left/Right)
            "CG_Height_m",          # Center of Gravity Height
            "Load_FL_N",            # Force Front Left
            "Load_FR_N",            # Force Front Right
            "Load_RL_N",            # Force Rear Left
            "Load_RR_N"             # Force Rear Right
        ]
        writer.writerow(headers)

        start_time = time.time()
        
        try:
            while True:
                # Read data
                phys = sim.physics
                
                # --- DATA MAPPING ---
                
                # 1. Time & Lap (We estimate lap from time or just use counter)
                current_time = round(time.time() - start_time, 3)
                # Note: Lap number isn't in the physics struct, usually in Graphics
                # We will use a placeholder '1' or you can add the Graphics struct if needed.
                # For simple physics analysis, time is usually sufficient.
                lap_num = 1 

                # 2. Engine
                rpm = int(phys.rpms)
                torque = round(phys.engine_torque, 2)
                
                # 3. Speed
                speed_ms = round(phys.speed_ms, 2)
                
                # 4. G-Forces (AC uses X=Lat, Z=Long usually, check sign)
                lat_g = round(phys.accG[0], 3)
                long_g = round(phys.accG[2], 3)
                
                # 5. Tilt (COG Analysis)
                pitch = round(phys.pitch, 4)
                roll = round(phys.roll, 4)
                cg_h = round(phys.cg_height, 3)
                
                # 6. Wheel Forces (Newtons)
                # Order: FL, FR, RL, RR
                w_fl = int(phys.wheel_load[0])
                w_fr = int(phys.wheel_load[1])
                w_rl = int(phys.wheel_load[2])
                w_rr = int(phys.wheel_load[3])

                # Write Row
                writer.writerow([
                    current_time, lap_num, rpm, torque, speed_ms,
                    lat_g, long_g, pitch, roll, cg_h,
                    w_fl, w_fr, w_rl, w_rr
                ])
                
                # 60 Hz Recording Rate (approx)
                time.sleep(0.016)

        except KeyboardInterrupt:
            print(f"\nStopped. Data saved to {filename}")
            sim.close()

if __name__ == "__main__":
    main()