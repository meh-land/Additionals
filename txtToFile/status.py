import random
import time


def Logs(filename):
    while True:
        try:
            x = random.randint(1, 100)  
            y = random.randint(1, 100)  
            theta = random.randint(1, 100)  
            
            with open(filename, 'a') as file:
                file.write(f"{x}, {y}, {theta}\n")
            
            print(f"Successfully appended {x, y, theta} to {filename}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(10)

# change path to be storage\app in dashboard backend  directory
filename = "C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Status.txt"
Logs(filename)