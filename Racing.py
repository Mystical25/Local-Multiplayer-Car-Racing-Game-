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

class user(AbstractCar):
    IMG = car
    start = (298,675)
    
def window(win, image, car,st,pt):
    win.blit(image[0],image[1])
    car.draw(win)
    timedraw(win,st)
    besttimedraw(win,pt)
    pygame.display.update()

def draw_rotate_center(win, image, position, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=position).center)
    win.blit(rotated_image, new_rect.topleft)

def timedraw(win,s):
    time_text = font.render(f"Time: {round(time.time()-s,2)}s", 1, (255, 255, 255))
    win.blit(time_text, (10,770))
def besttimedraw(win,p):
    time_text = font.render(f"Best Time: {p}s", 1, (255, 255, 255))
    win.blit(time_text, (10,730))

pcar=user(3.3,3)

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

def main():
    clock = pygame.time.Clock()
    run = True
    start_time=time.time()
    best_time=1000
    flag=False
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        movecar(pcar)
        window(WIN, bgimages, pcar,start_time,best_time)
        if pcar.collide(track_mask) != None:
            pcar.bounce()
        if pcar.collide(finish_flag_mask) != None:
            flag=True
        if pcar.collide(finish_mask) != None:
            if flag:
                flag=False
                pcar.restart()
                new_time = round(time.time()-start_time,2)
                if new_time<best_time:
                    best_time=new_time
                start_time=time.time()
            else:
                pcar.bounce()

    pygame.quit()
    return(best_time)

print("Your best lap time was :",main(),"s")