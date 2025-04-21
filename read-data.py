import BAC0
import json
import time
import sys

# Data dictionary to store values
data = {
    "local_device": {},
    "remote_device": {}
}

def main():
    try:
        # Create a bacnet connection with error handling
        # Use your IP address for the network connection
        bacnet = BAC0.lite(ip="192.168.151.186/24", port=47809)
        print("BAC0 connection established successfully")
        
        # Add a brief pause to ensure network is ready
        time.sleep(2)
        
        # Define simulator details
        local_simulator = {
            "address": "192.168.151.186:58011",
            "name": "local_device"
        }
        
        remote_simulator = {
            "address": "192.168.151.24:58956",
            "name": "remote_device"
        }
        
        simulators = [local_simulator, remote_simulator]
        
        while True:
            try:
                for simulator in simulators:
                    print(f"Reading from {simulator['name']} at {simulator['address']}...")
                    
                    # Reading 3 Analog Inputs from each simulator
                    for x in range(0, 3):
                        id = str(x)
                        try:
                            # Read from the simulator
                            value = bacnet.read(
                                f"{simulator['address']} analogInput {id} presentValue")
                            print(f"{simulator['name']} - Analog input {id} value: {value}")
                            value = str(value)
                            data[simulator['name']][f"Analog_input{id}"] = value
                        except Exception as e:
                            print(f"Error reading analog input {id} from {simulator['name']}: {e}")
                            data[simulator['name']][f"Analog_input{id}"] = "Error reading value"
                
                # print("\nCurrent data from all devices:")
                # print(json.dumps(data, indent=2))
                # print("\n" + "-"*50 + "\n")
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