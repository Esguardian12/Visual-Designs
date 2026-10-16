import pygame, random, math, time, sys

W, H = 1000, 700
pygame.init()
s = pygame.display.set_mode((W, H), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("HELIX_RECON_V16")
c = pygame.time.Clock()
t0 = time.time()
G, WHT, BLK = (0, 255, 0), (255, 255, 255), (0, 0, 0)
fx = pygame.Surface((W, H), pygame.SRCALPHA)

def lerp(a, b, f):
    return a + (b - a) * f

def clip(v, l):
    return max(-1, min(1, int(v)))

class HelixNode:
    def __init__(self, y, off, cl):
        self.y = y
        self.off = off
        self.cl = cl
        self.h = []

    def draw(self, surf, t, ry, tx, f, sh):
        ang = t * 3 + self.y * 0.01 + self.off
        x = math.cos(ang) * 200
        z = math.sin(ang) * 200
        y = self.y
        
        rx = x * math.cos(ry) - z * math.sin(ry)
        rz = x * math.sin(ry) + z * math.cos(ry)
        ry_n = y * math.cos(tx) - rz * math.sin(tx)
        rz_n = y * math.sin(tx) + rz * math.cos(tx)
        
        v = f / max(1, rz_n + 2500)
        
        # Clean mathematical projections assigned explicitly
        px = int(W / 2 + rx * v + sh)
        py = int(H / 2 + ry_n * v + sh)
        
        sz = max(1, int(12 * v))
        if self.cl == WHT and random.random() > 0.8:
            sz *= 2
            pygame.draw.circle(surf, WHT, (px, py), sz)
        else:
            pygame.draw.rect(surf, self.cl, (px - sz // 2, py - sz // 2, sz, sz), 0)
            
        return px, py, v

def run():
    nodes = []
    for y in range(-400, 401, 15):
        nodes.append(HelixNode(y, 0, G))
        nodes.append(HelixNode(y, math.pi, G))
        if y % 45 == 0:
            nodes.append(HelixNode(y, 0, WHT))
            
    fade = pygame.Surface((W, H))
    fade.fill(WHT)
    
    while True:
        now = time.time() - t0
        if now >= 15.0:
            break
            
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if now > 14.0 and len(nodes) > 20:
            nodes = nodes[:int(len(nodes) * 0.7)]
            
        s.fill(BLK)
        fx.fill((0, 0, 0, 0))
        ry, tx = now * 1.2, math.sin(now * 0.5) * 0.4
        sh = int(math.sin(now * 150) * 40) if now > 13.0 else 0
        
        pts = []
        for n in nodes:
            px, py, v = n.draw(fx, now, ry, tx, 6000, sh)
            pts.append((px, py, v, n.cl))
            
        if now < 14.0:
            for i in range(0, len(pts) - 2, 2):
                p1, p2 = pts[i], pts[i + 1]
                if p1[2] > 0.1:
                    pygame.draw.line(fx, (*G, 60), (p1[0], p1[1]), (p2[0], p2[1]), 1)
                    
        scan_y = int((now * 400) % H)
        pygame.draw.line(fx, (*G, 120), (0, scan_y), (W, scan_y), 2)
        s.blit(fx, (0, 0))
        
        if now > 14.3:
            a = int(min(255, (now - 14.3) * 425))
            fade.set_alpha(a)
            s.blit(fade, (0, 0))
            
        pygame.display.flip()
        c.tick(60)

if __name__ == "__main__":
    run()
    pygame.quit()
