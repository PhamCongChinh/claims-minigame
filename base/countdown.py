import time

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Thời gian chờ còn: {timer}", end="\r")
        time.sleep(1)
        t-=1
    print('Fire in the hole!!')