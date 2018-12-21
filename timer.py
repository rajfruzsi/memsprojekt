import time
import schedule

def job():
    print(m)

schedule.every(0.1).minutes.do(job)

c=0

while True:
    c+=1
    m="Hello "+str(c)
    schedule.run_pending()

