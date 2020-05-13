#Bot class
import subprocess as s
from time import *
from threading import Thread

class Bot:

    def __init__(self, chrom, id, port, typ, limit):
        self.chrom = chrom
        self.id = id
        self.port = port
        self.typ = typ
        self.limit = limit
    
    def server(self):
        if self.typ == 1:
            ser = ["./xpilots", "-map", "maps/simple.xp",\
                "-noQuit", "-switchBase", "1", "-maxrobots", "0", "-framespersecond", "30", "-maxClientsPerIP", "2", "-port", str(self.port)]
        elif self.typ == 2:
            ser = ["./xpilots", "-map", "maps/simple_atk.xp",\
                "-noQuit", "-switchBase", "1", "-maxrobots", "0", "-framespersecond", "30", "-maxClientsPerIP", "2", "-port", str(self.port)]
        elif self.typ == 3:
            ser = ["./xpilots", "-map", "maps/simple_def3.xp",\
                "-noQuit", "-switchBase", "1", "-maxrobots", "9", "-framespersecond", "30", "-maxClientsPerIP", "2", "-port", str(self.port)]
        self.p = s.Popen(ser)

    def sKill(self):
        self.p.kill()

    def test(self):
        if self.typ == 1:
            bot = ["python3 Dumbo.py runBot " + self.nSChrom() + " " + str(self.id) + " " + str(self.port) + " " + str(self.typ) + " " + str(self.limit)]
            self.b = s.Popen(bot, shell = True)
            self.b.wait()
        elif self.typ == 2:
            bot = ["python3 Dumbo.py runBot " + self.nSChrom() + " " + str(self.id) + " " + str(self.port) + " " + str(self.typ) + " " + str(self.limit)]
            ebot = ["python3 Dumbo_noshoot.py runBot " + " " + str(self.port) + " " + str(self.limit)]
            self.b = s.Popen(bot, shell = True)
            self.eb = s.Popen(ebot, shell = True)
            self.b.wait()
        elif self.typ == 3:
            bot = ["python3 Dumbo.py runBot " + self.nSChrom() + " " + str(self.id) + " " + str(self.port) + " " + str(self.typ) + " " + str(self.limit)]
            self.b = s.Popen(bot, shell = True)
            self.b.wait()

        

    def nSChrom(self):
        out = "["
        for i in self.chrom:
            out = out + str(i)+","
        out = out[:-1] + "]"
        return out

    def run(self):
        self.server()
        self.test()
        self.sKill()

    def getID(self):
        return self.id

def main():
    
    lst = []
    for i in range(3):
        b = Bot([i,0,0,0], i + 1, 15350 + i)
        lst.append(b)
    for i in lst:
        Thread(target = i.run).start()

    print("done")

if __name__ == '__main__':
    main()