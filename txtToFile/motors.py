import random
import time


def Logs(filename):
    while True:
        try:
            m1 = random.randint(1, 100)  
            m2 = random.randint(1, 100)  
            m3 = random.randint(1, 100)
            m4 = random.randint(1, 100)  
            
            with open(filename, 'a') as file:
                file.write(f"{m1}, {m2}, {m3}, {m4}\n")
            
            print(f"Successfully appended {m1, m2, m3, m4} to {filename}.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(1)

# change path to be storage\app in dashboard backend  directory
filename = "C:\\xampp\\htdocs\\dashboard_ros\\storage\\app\\Motors.txt"
Logs(filename)