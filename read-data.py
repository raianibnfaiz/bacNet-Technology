import BAC0
import json
import time
import sys

# Data dictionary to store values
data = {}

def main():
    try:
        # Create a bacnet connection with error handling
        bacnet = BAC0.lite(ip="192.168.50.58/24", port=47809)
        print("BAC0 connection established successfully")
        
        # Add a brief pause to ensure network is ready
        time.sleep(2)
        
        while True:
            try:
                # Reading 3 Objects from the Bacnet Simulator
                for x in range(0, 3):
                    id = str(x)
                    # Connect to the BACnet simulator using the IP address and port number
                    try:
                        value = bacnet.read(
                            "192.168.50.58:53970 analogInput "+id+" presentValue")
                        # value = bacnet.read(
                        #     "192.168.50.58:52134 analogInput "+id+" presentValue")
                        print(f"Aanalog input {id} value: {value}")
                        value = str(value)
                        data["Analog_input"+id] = value
                    except Exception as e:
                        print(f"Error reading analog input {id}: {e}")
                        data["Analog_input"+id] = "Error reading value"

                print(json.dumps(data, indent=2))
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("User interrupted the process")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying
    
    except Exception as e:
        print(f"Error initializing BAC0: {e}")
    finally:
        # Clean up BAC0 connection if it exists
        try:
            if 'bacnet' in locals():
                bacnet.disconnect()
                print("BAC0 connection closed")
        except:
            pass

# RUN main
if __name__ == '__main__':
    main()