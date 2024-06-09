import random
import time


def Logs(filename):
    while True:
        try:
            random_number = random.randint(1, 100)  
            
            with open(filename, 'a') as file:
                file.write(f"{random_number}\n")
            
            print(f"Successfully appended {random_number} to {filename}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(10)

# change path to be storage\app in dashboard backend  directory
filename = "C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Logs.txt"
Logs(filename)