import time

for i in range(10):
    print(f"Count: {i}", end='\r', flush=True) 
    time.sleep(0.5)