'''
Created on 2011-5-5

@author: Robin
'''
db = []
history_file = "history.txt"
def build_db():
    with open(history_file) as f:
        for line in f:
            s = line.split()
            sn = s[0]
            blue = s[-7:-1]
            red = s[-1:]
            db.append([sn, blue, red])


build_db()       
blue = {}
total_b = 0
red = {}
total_r = 0

with open("r.txt", 'w') as rec:
    for l in db:
        bb = l[1]
        for b in l[1]:
            b = int(b)
            total_b += 1
            if b not in blue:
                blue[b] = 1
            else:
                blue[b] += 1
                
        for c in bb:
            c = int(c)
            line = "blue[%s]=%s rate=%s\t ave=%s\n"%(c,blue[c],blue[c]/(total_b/6), total_b/33)
            rec.write(line)
                
        for r in l[2]:
            r = int(r)
            total_r += 1
            if r not in red:
                red[r] = 1
            else:
                red[r] += 1
            line = "red[%s]=%s ave=%s\n"%(r,red[r],total_r/16)
            rec.write(line)
            
for i in range(1,34):
    print("%s \toccurs \t%s times\t %s"%(i, blue[i], total_b/33))
    
print("------------------------------------------")

for r in range(1, 17):
    print("%s \toccurs \t%s times\t %s"%(r, red[r], total_r/16))

print("ratio %s"%(1/(33*32*31*30*29*28*16)))
