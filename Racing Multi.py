import pygame
import time
import math
pygame.font.init()

white=(255,255,255)

bg = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\TRACK.png"),(800,800))
bgcoord=(0,0)
bgimages=(bg,bgcoord)

track = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\TRACK_BORDER.png"),(800,800))
track_mask=pygame.mask.from_surface(track)

finish = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\FINISH.png"),(800,800))
finish_mask=pygame.mask.from_surface(finish)

finish_flag = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\FINISH_FLAG.png"),(800,800))
finish_flag_mask=pygame.mask.from_surface(finish_flag)

font = pygame.font.SysFont("Roboto", 44)

car = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\CAR.png"),(15, 25))
car2 = pygame.transform.scale(pygame.image.load("C:\\Users\\Mystical\\Python\\Bonus Project\\CAR2.png"),(15, 25))

WIN = pygame.display.set_mode((800,800))
pygame.display.set_caption("FIRST GAME")
    
class AbstractCar:
    def __init__(self,maxvel,rotvel):
        self.img = self.IMG
        self.maxvel = maxvel
        self.vel = 0
        self.rotvel = rotvel
        self.angle = 90
        self.x,self.y = self.start
        self.acceleration = 0.1
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotvel
        elif right:
            self.angle -= self.rotvel
    def draw(self,win):
        draw_rotate_center(win,self.img,(self.x,self.y),self.angle)
    def moveforward(self):
        self.vel = min(self.vel + self.acceleration, self.maxvel)
        self.move()
    def movebackward(self):
        self.vel = max(self.vel - self.acceleration, -self.maxvel/2)
        self.move()
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians)*self.vel
        self.y -= vertical
        self.x -= horizontal
    def friction(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move()
    def collide(self,mask,x=0,y=0):
        car_mask=pygame.mask.from_surface(self.img)
        offset=[int(self.x-x),int(self.y-y)]
        collision=mask.overlap(car_mask,offset)
        return collision
    def bounce(self):
        self.vel=-self.vel
        self.move()
    def restart(self):
        self.x,self.y=self.start
    def stop(self):
        self.vel=0

class p1(AbstractCar):
    IMG = car
    start = (298,665)
class p2(AbstractCar):
    IMG = car2
    start = (298,685)

def window(win, image, car, car2, st, p1t, p2t, s):
    win.blit(image[0],image[1])
    car.draw(win)
    car2.draw(win)
    scoredraw(win,s)
    timedraw(win,st)
    besttime1draw(win,p1t)
    besttime2draw(win,p2t)
    pygame.display.update()

def draw_rotate_center(win, image, position, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=position).center)
    win.blit(rotated_image, new_rect.topleft)

def timedraw(win,s):
    time_text = font.render(f"Time: {round(time.time()-s,2)}s", 1, white)
    win.blit(time_text, (10,20))
def besttime1draw(win,p):
    time_text = font.render(f"Best Time P1: {p}s", 1, white)
    win.blit(time_text, (30,770))
def besttime2draw(win,p):
    time_text = font.render(f"Best Time P2: {p}s", 1, white)
    win.blit(time_text, (440,770))
def scoredraw(win,s):
    score_text=font.render(f"P1  {s[0]} - {s[1]}  P2", 1, white)
    win.blit(score_text, (370,30))

pcar1=p1(3.3,3)
pcar2=p2(3.3,3)

def movecar(pcar):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        pcar.rotate(left=True)
    if keys[pygame.K_d]:
        pcar.rotate(right=True)
    if keys[pygame.K_w]:
        moved=True
        pcar.moveforward()
    if keys[pygame.K_s]:
        moved=True
        pcar.movebackward()
    if not moved:
        pcar.friction()

def movecar2(pcar):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT]:
        pcar.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        pcar.rotate(right=True)
    if keys[pygame.K_UP]:
        moved=True
        pcar.moveforward()
    if keys[pygame.K_DOWN]:
        moved=True
        pcar.movebackward()
    if not moved:
        pcar.friction()

def main():
    clock = pygame.time.Clock()
    run = True
    start_time=time.time()
    best_time_1=1000
    best_time_2=1000
    flag1=False
    flag2=False
    finish1=False
    finish2=False
    lap_time_1=0
    lap_time_2=0
    scores=[0,0]
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        movecar(pcar1)
        movecar2(pcar2)
        window(WIN, bgimages, pcar1, pcar2,start_time,best_time_1,best_time_2,scores)

        if pcar1.collide(track_mask) != None:
            pcar1.bounce()
        if pcar2.collide(track_mask) != None:
            pcar2.bounce()
        if pcar1.collide(finish_flag_mask) != None:
            flag1=True
        if pcar2.collide(finish_flag_mask) != None:
            flag2=True
        if pcar2.collide(finish_mask) != None and not finish2:
            if flag2:
                finish2=True
                pcar2.stop()
                lap_time_2 = round(time.time()-start_time,2)
                if lap_time_2<best_time_2:
                    best_time_2=lap_time_2
            else:
                pcar2.bounce()
        if pcar1.collide(finish_mask) != None and not finish1:
            if flag1:
                finish1=True
                pcar1.stop()
                lap_time_1 = round(time.time()-start_time,2)
                if lap_time_1<best_time_1:
                    best_time_1=lap_time_1
            else:
                pcar2.bounce()

        if finish1:
            pcar1.stop()
        if finish2:
            pcar2.stop()

        if finish1 and finish2:
            if lap_time_1<lap_time_2:
                scores[0]+=1
            elif lap_time_2<lap_time_1:
                scores[1]+=1
            window(WIN, bgimages, pcar1, pcar2,start_time,best_time_1,best_time_2,scores)
            pcar1.restart()
            pcar2.restart()
            flag1=flag2=finish1=finish2=False
            start_time=time.time()

    pygame.quit()

main()