import random, math, sys
from importlib import import_module

try:
    pygame = import_module("pygame")
except ModuleNotFoundError as exc:
    if exc.name != "pygame":
        raise
    raise SystemExit("AudioRipple requires pygame; install it with `python -m pip install pygame`.") from exc
W,H = 1000, 700
pygame.init()
s = pygame.display.set_mode((W,H), pygame.DOUBLEBUF|pygame.HWSURFACE)
c = pygame.time.Clock()
G,WHT,BLK = (0,255,0),(255,255,255),(0,0,0)
class AudioEqualizer:
    def __init__(self):
        self.bars = 64
    def process(self, sf, f):
        bass = math.sin(f*0.25)*4 if f%30<15 else math.cos(f*0.15)
        bass = max(0, bass+4)
        pts_inner, pts_outer = [],[]
        for i in range(self.bars):
            ang = i * (math.pi* 2/self.bars) + f*0.01
            r_in = 120 + math.sin(f * 0.05 + i) * 2
            r_out = 120 + bass * 6 + math.sin(f * 0.1 + i) * 8
            cx, cy = W//2, H//2
            pts_inner.append((int(cx + math.cos(ang)*r_in), int(cy + math.sin(ang) * r_in)))
            pts_outer.append((int(cx + math.cos(ang)*r_out), int(cy + math.sin(ang) * r_out)))
        for i in range(self.bars):
            pygame.draw.line(sf, G, pts_inner[i], pts_outer[i], 2)
        if len(pts_inner) > 2:
            pygame.draw.polygon(sf, (0, 40, 0). pts_inner, 0)
            pygame.draw.polygon(sf, WHT,pts_inner, 2)

class ThermalRipple:
    def __int__(self):
        self.rings=[]
    def process(self, sf, f):
        if f % 15 == 0:
            self.rings.append([120,255])
        for r in self.rings:
            r[0] += 4
            r[1] -= 5
            if r[0] > 500:
                self.rings.remove(r)
                continue
            if r[1] > 0:
                pygame.draw.circle(sf, (*G, r[1]), (W//2, H//2), int(r[0]), 1)

class FrequencySwarm:
    def __init__(self):
        self.p = [[random.uniform(0,W),
                   random.uniform(0,H),
                   random.uniform(2,5)]
                    for _ in range(120)]
    def process(self, sf, f):
        bass = math.sin(f * 0.25) * 6 if f % 30 < 15 else math.cos( f * 0.15) * 10
        for p in self.p:
            p[1] -= p[2]
            p[0] += math.sin(f * 0.05 + p[1] * 0.01) * 1.5
            if p[1] < 0:
                p[1] = H
                p[0] = random.uniform(0,W)
            sz = 1 if p[2] < 3 else 2
            al = int (150 + bass * 10)
            al = max(50, min(255, al))
            pygame.draw.circle(sf,(*WHT,al), (int(p[0]), int(p[1])), sz)

def main():
    eq, ripple, swarm, f = AudioEqualizer(), ThermalRipple(), FrequencySwarm(), 0
    while f < 900:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:pygame.quit();sys.exit()
        s.fill(BLK)
        ripple.process(s,f)
        eq.process(s,f)
        swarm.process(s,f)
        if f%30 < 4 and f > 180:
            s.blit(s, random.randint(-8,8),
                        random.randint(-2,2),
                        special_flags=pygame.BLEND_RGB_ADD)
        pygame.display.flip()
        c.tick(60)
        f += 1
if __name__=="__main__":
    try:main()
    except:pass
    finally:pygame.quit(); sys.exit() 
