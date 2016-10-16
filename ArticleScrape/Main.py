import threading
import NewsDate
import GooGNewsDate

threadlist = []

t = threading.Thread(target = NewsDate)
t.start()
threadlist.append(t)

t = threading.Thread(target = GooGNewsDate)
t.start()
threadlist.append(t)

for b in threadlist:
    b.join()

