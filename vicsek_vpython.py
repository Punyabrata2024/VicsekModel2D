Web VPython 3.2
import random as rr


g = graph(title="avg_v vs t", xtitle="t", ytitle = "avg_v")
f1 = gcurve(color=color.blue, dot = True)
canvas(title="Flocking behaviour simulation using boid algorithm",width=800, height = 600, background=color.white)

N = 100#No. of birds
v0=0.3#speed of each bird
R =1#interaction radius
r = 0#separation radius to avoid collision
eta = .5#noise
particles=[]
arrows=[]
L=5#to scale the canvas - area of flocking
vscale = 0.1
t= 0#time
dt = 0.01
circle = ring(pos=vector(0,0,0),axis=vector(0,0,1), radius = R, thickness = 0.1, color = color.black)
circle2 = ring(pos=vector(0,0,0),axis=vector(0,0,1), radius = r, thickness = 0.1, color = color.red)
def rand():#to generate -1 or 1 randomly for assigning random positions and directions of motion during initialisation
  
  if random()<0.5:
    c = -1
  else:
    c=1
  return c
  
for i in range(N):#initialising
  angle = random()*pi*rand()
  particle = sphere(pos=L*vector.random()*rand(), radius = 0.01, color=color.black)
  particle.pos.z=0
  particle.v = v0*vector(cos(angle),sin(angle),0)
  myarrow=arrow(pos=particle.pos, axis=vscale*norm(particle.v), color=color.black)
  particles.append(particle)
  arrows.append(myarrow)
  print (particle.v)

def update_positions():
 
  for i in range(N):
    neighbours =[]
    neighb = []
    for j in range(N):#to detect neighbours
      if i!=j and mag(particles[j].pos-particles[i].pos)<R:
        neighbours.append(particles[j].v)
        neighb.append(particles[j])
    avg_dir = vector(0,0,0)
    if len(neighbours)!= 0:
      for neigh_v in neighbours:#calculating avg direction of motion of neighbours in interaction radius
        avg_dir += neigh_v
      avg_dir = avg_dir/len(neighbours)
    noise = random()*eta*rand()/2 #generating a random noise
    new_angle = atan2(avg_dir.y,avg_dir.x) + noise #new angle for alignment in flock
    if len(neighbours)!= 0:
      particles[i].v = v0*vector(cos(new_angle),sin(new_angle),0)#updating velocities
    particles[i].pos += particles[i].v*dt#updating positions
    
    if particles[i].pos.x>L:
      particles[i].pos.x -= 2*L
    if particles[i].pos.x<-L:
      particles[i].pos.x += 2*L
    if particles[i].pos.y>L:
      particles[i].pos.y -= 2*L
    if particles[i].pos.y<-L:
      particles[i].pos.y += 2*L
    for neighbor in neighb:

    arrows[i].pos=particles[i].pos
    arrows[i].axis=vscale*particles[i].v
    circle.v=particles[N/2].v
    circle.pos=particles[N/2].pos
    circle2.v=particles[N/2].v
    circle2.pos=particles[N/2].pos

avg_v = vector(0,0,0)
net_dir= arrow(pos=vector(0,0,0),axis=avg_v, color=color.red)


while True:
  rate(20)
  update_positions()
  t = t+dt
  for i in range(N):
    avg_v = avg_v + particles[i].v
  avg_v /= N
  net_dir.axis=avg_v
  print ("The magnitude of average velocity of net movement is", mag(avg_v), "corresponds to", avg_v)
  f1.plot(t,mag(avg_v))
