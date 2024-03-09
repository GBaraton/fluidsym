import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import imageio
import time


def base_wave(rho, rho0):
  for i in range(len(rho)):
    for j in range(len(rho[0])):
      rho[i,j] = rho0+.01*np.sin(2*np.pi*i/len(rho) + 2*np.pi*j/len(rho[0]))
  return rho

def base_checkers(rho, rho0):
  for i in range(len(rho)):
    for j in range(len(rho[0])):
      rho[i,j] = rho0+.01*(np.sin(6*np.pi*i/len(rho) ) + np.sin(6*np.pi*j/len(rho[0])))
  return rho


def mass_check(rho):
  return np.sum(rho)


def init(f, f_eq, rho, ux, uy, w_a, d_cs2, d_cs4):
    f_eq[ 0, :, : ] = rho[:,:] * w_a[0] * (1 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2))
    f_eq[ 1, :, : ] = rho[:,:] * w_a[1] * (1 + d_cs2*ux[:,:] + .5*d_cs4*ux[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 2, :, : ] = rho[:,:] * w_a[2] * (1 + d_cs2*uy[:,:] + .5*d_cs4*uy[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 3, :, : ] = rho[:,:] * w_a[3] * (1 - d_cs2*ux[:,:] + .5*d_cs4*ux[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 4, :, : ] = rho[:,:] * w_a[4] * (1 - d_cs2*uy[:,:] + .5*d_cs4*uy[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 5, :, : ] = rho[:,:] * w_a[5] * (1 + d_cs2*( ux[:,:]+uy[:,:]) + .5*d_cs4*( ux[:,:]+uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 6, :, : ] = rho[:,:] * w_a[6] * (1 + d_cs2*(-ux[:,:]+uy[:,:]) + .5*d_cs4*(-ux[:,:]+uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 7, :, : ] = rho[:,:] * w_a[7] * (1 + d_cs2*(-ux[:,:]-uy[:,:]) + .5*d_cs4*(-ux[:,:]-uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 8, :, : ] = rho[:,:] * w_a[8] * (1 + d_cs2*( ux[:,:]-uy[:,:]) + .5*d_cs4*( ux[:,:]-uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f = np.copy(f_eq)
    return(f, f_eq)


def collision(f, f_eq, rho, ux, uy, w_a, d_cs2, d_cs4, d_Tau):
    f_eq[ 0, :, : ] = rho[:,:] * w_a[0] * (1 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2))
    f_eq[ 1, :, : ] = rho[:,:] * w_a[1] * (1 + d_cs2*ux[:,:] + .5*d_cs4*ux[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 2, :, : ] = rho[:,:] * w_a[2] * (1 + d_cs2*uy[:,:] + .5*d_cs4*uy[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 3, :, : ] = rho[:,:] * w_a[3] * (1 - d_cs2*ux[:,:] + .5*d_cs4*ux[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 4, :, : ] = rho[:,:] * w_a[4] * (1 - d_cs2*uy[:,:] + .5*d_cs4*uy[:,:]**2 - .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 5, :, : ] = rho[:,:] * w_a[5] * (1 + d_cs2*( ux[:,:]+uy[:,:]) + .5*d_cs4*( ux[:,:]+uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 6, :, : ] = rho[:,:] * w_a[6] * (1 + d_cs2*(-ux[:,:]+uy[:,:]) + .5*d_cs4*(-ux[:,:]+uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 7, :, : ] = rho[:,:] * w_a[7] * (1 + d_cs2*(-ux[:,:]-uy[:,:]) + .5*d_cs4*(-ux[:,:]-uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )
    f_eq[ 8, :, : ] = rho[:,:] * w_a[8] * (1 + d_cs2*( ux[:,:]-uy[:,:]) + .5*d_cs4*( ux[:,:]-uy[:,:])**2- .5*d_cs2*(ux[:,:]**2 + uy[:,:]**2)  )

    f[0, :, :] = f[0, :, :]*(1 - d_Tau) + f_eq[0, :, :]*d_Tau
    f[1, :, :] = f[1, :, :]*(1 - d_Tau) + f_eq[1, :, :]*d_Tau
    f[2, :, :] = f[2, :, :]*(1 - d_Tau) + f_eq[2, :, :]*d_Tau
    f[3, :, :] = f[3, :, :]*(1 - d_Tau) + f_eq[3, :, :]*d_Tau
    f[4, :, :] = f[4, :, :]*(1 - d_Tau) + f_eq[4, :, :]*d_Tau
    f[5, :, :] = f[5, :, :]*(1 - d_Tau) + f_eq[5, :, :]*d_Tau
    f[6, :, :] = f[6, :, :]*(1 - d_Tau) + f_eq[6, :, :]*d_Tau
    f[7, :, :] = f[7, :, :]*(1 - d_Tau) + f_eq[7, :, :]*d_Tau
    f[8, :, :] = f[8, :, :]*(1 - d_Tau) + f_eq[8, :, :]*d_Tau

    return f, f_eq

def stream(f, f_new):
    f_new[0,  :  ,  :  ] = f[0,  :  ,  :  ] 

    f_new[1, 1:  ,  :  ] = f[1,  :-1,  :  ] 
    f_new[2,  :  , 1:  ] = f[2,  :  ,  :-1] 
    f_new[3,  :-1,  :  ] = f[3, 1:  ,  :  ] 
    f_new[4,  :  ,  :-1] = f[4,  :  , 1:  ] 

    f_new[5, 1:  , 1:  ] = f[5,  :-1,  :-1] 
    f_new[6,  :-1, 1:  ] = f[6, 1:  ,  :-1] 
    f_new[7,  :-1,  :-1] = f[7, 1:  , 1:  ] 
    f_new[8, 1:  ,  :-1] = f[8,  :-1, 1:  ] 

    f = np.copy(f_new)
    return(f)

def BC_perio(f):
    #left
    f[1, 0,  :  ] = f[1,-1,  :  ] 
    f[5, 0,  :  ] = f[5,-1,  :  ] 
    f[8, 0,  :  ] = f[8,-1,  :  ] 

    #right
    f[3,-1,  :  ] = f[3, 0,  :  ] 
    f[6,-1,  :  ] = f[6, 0,  :  ] 
    f[7,-1,  :  ] = f[7, 0,  :  ]  

    #bot
    f[2,  :  , 0] = f[2,  :  ,-1] 
    f[5,  :  , 0] = f[5,  :  ,-1] 
    f[6,  :  , 0] = f[6,  :  ,-1] 

    #top
    f[4,  :  ,-1] = f[4,  :  , 0]  
    f[8,  :  ,-1] = f[8,  :  , 0] 
    f[7,  :  ,-1] = f[7,  :  , 0] 

    #left
    #f[1, 0,  :  ] = f[1,-1,  :  ] 
    #f[5, 0, 1:  ] = f[5,-1,  :-1] 
    #f[8, 0,  :-1] = f[8,-1, 1:  ] 

    #right
    #f[3,-1,  :  ] = f[3, 0,  :  ] 
    #f[6,-1, 1:  ] = f[6, 0,  :-1] 
    #f[7,-1,  :-1] = f[7, 0, 1:  ]  

    #bot
    #f[2,  :  , 0] = f[2,  :  ,-1] 
    #f[5, 1:  , 0] = f[5,  :-1,-1] 
    #f[6,  :-1, 0] = f[6, 1:  ,-1] 

    #top
    #f[4,  :  ,-1] = f[4,  :  , 0]  
    #f[8, 1:  ,-1] = f[8,  :-1, 0] 
    #f[7,  :-1,-1] = f[7, 1:  , 0] 


    #corners

    #f[5,  0,  0] = f[5, -1, -1]  
    #f[6, -1,  0] = f[6,  0, -1] 
    #f[7, -1, -1] = f[7,  0,  0] 
    #f[8,  0, -1] = f[8, -1,  0] 
    return(f)

def BC_wall(f):    
  #left
    f[1, 0,  :  ] = f[3, 0,  :  ] 
    f[5, 0,  :  ] = f[6, 0,  :  ] 
    f[8, 0,  :  ] = f[7, 0,  :  ] 

    #right
    f[3,-1,  :  ] = f[1,-1,  :  ] 
    f[6,-1,  :  ] = f[5,-1,  :  ] 
    f[7,-1,  :  ] = f[8,-1,  :  ]  

    #bot
    f[2,  :  , 0] = f[4,  :  , 0] 
    f[5,  :  , 0] = f[8,  :  , 0] 
    f[6,  :  , 0] = f[7,  :  , 0] 

    #top
    f[4,  :  ,-1] = f[2,  :  ,-1]  
    f[8,  :  ,-1] = f[5,  :  ,-1] 
    f[7,  :  ,-1] = f[6,  :  ,-1]  
    return(f)


def BC_channel(f):
    #left
    f[1, 0,  :  ] = f[1,-1,  :  ] 
    f[5, 0,  :  ] = f[5,-1,  :  ] 
    f[8, 0,  :  ] = f[8,-1,  :  ] 

    #right
    f[3,-1,  :  ] = f[3, 0,  :  ] 
    f[6,-1,  :  ] = f[6, 0,  :  ] 
    f[7,-1,  :  ] = f[7, 0,  :  ]  

    #bot
    f[2,  :  , 0] = f[4,  :  , 0] 
    f[5,  :  , 0] = f[8,  :  , 0] 
    f[6,  :  , 0] = f[7,  :  , 0] 

    #top
    f[4,  :  ,-1] = f[2,  :  ,-1]  
    f[8,  :  ,-1] = f[5,  :  ,-1] 
    f[7,  :  ,-1] = f[6,  :  ,-1]
    return(f)


def BC_driven_channel(f, rho, d_cs2, w_a):
    #left
    f[1, 0,  :  ] = f[1,-1,  :  ] 
    f[5, 0,  :  ] = f[5,-1,  :  ] 
    f[8, 0,  :  ] = f[8,-1,  :  ] 

    #right
    f[3,-1,  :  ] = f[3, 0,  :  ] 
    f[6,-1,  :  ] = f[6, 0,  :  ] 
    f[7,-1,  :  ] = f[7, 0,  :  ]  

    #bot
    f[2,  :  , 0] = f[4,  :  , 0] 
    f[5,  :  , 0] = f[7,  :  , 0] - 2 * w_a[7] * rho[:, 1] * d_cs2 * -.37
    f[6,  :  , 0] = f[8,  :  , 0] - 2 * w_a[8] * rho[:, 1] * d_cs2 *  .37

    #top
    f[4,  :  ,-1] = f[2,  :  ,-1]  
    f[8,  :  ,-1] = f[6,  :  ,-1] - 2 * w_a[6] * rho[:,-2] * d_cs2 * -.37
    f[7,  :  ,-1] = f[5,  :  ,-1] - 2 * w_a[5] * rho[:,-2] * d_cs2 *  .37
    return(f)

def BC_driven_channel_vp(f, rho, d_cs2, d_cs4, w_a, ux, uy):
    #NE MARCHE PAS!
    #vinlet
    f[1, 0,  :  ] = f[3, 0,  :  ] - 2 * w_a[3] * rho[ 1,:] * d_cs2 * -.3
    f[5, 0,  :  ] = f[6, 0,  :  ] - 2 * w_a[6] * rho[ 1,:] * d_cs2 * -.3
    f[8, 0,  :  ] = f[7, 0,  :  ] - 2 * w_a[7] * rho[ 1,:] * d_cs2 * -.3

    #poutlet
    f[3,-1,  :  ] =-f[1,-1,  :  ] + 2 * w_a[1] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )
    f[6,-1,  :  ] =-f[5,-1,  :  ] + 2 * w_a[5] * rho[-2,:] * (1 + .5*d_cs4*(  ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]) + uy[-2,:]-.5*(uy[-2,:]-uy[-3,:])  )**2 - .5*d_cs2*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]) + uy[-2,:]-.5*(uy[-2,:]-uy[-3,:]))**2     )
    f[7,-1,  :  ] =-f[8,-1,  :  ] + 2 * w_a[8] * rho[-2,:] * (1 + .5*d_cs4*(  ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]) - uy[-2,:]+.5*(uy[-2,:]-uy[-3,:])  )**2 - .5*d_cs2*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]) + uy[-2,:]-.5*(uy[-2,:]-uy[-3,:]))**2     )

    #poutlet
    #f[3,-1,  :  ] =-f[1,-1,  :  ] + 2 * w_a[1] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )
    #f[6,-1,  :  ] =-f[5,-1,  :  ] + 2 * w_a[5] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )
    #f[7,-1,  :  ] =-f[8,-1,  :  ] + 2 * w_a[8] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )

    #bot
    f[2,  :  , 0] = f[4,  :  , 0] 
    f[5,  :  , 0] = f[7,  :  , 0] - 2 * w_a[7] * rho[:, 1] * d_cs2 * -.3
    f[6,  :  , 0] = f[8,  :  , 0] - 2 * w_a[8] * rho[:, 1] * d_cs2 *  .3

    #top
    f[4,  :  ,-1] = f[2,  :  ,-1]  
    f[8,  :  ,-1] = f[6,  :  ,-1] - 2 * w_a[6] * rho[:,-2] * d_cs2 * -.3
    f[7,  :  ,-1] = f[5,  :  ,-1] - 2 * w_a[5] * rho[:,-2] * d_cs2 *  .3
    return(f)

def BC_driven_channel_vv(f, rho, d_cs2, d_cs4, w_a):
    #NE MARCHE PAS!
    #vinlet
    f[1, 0,  :  ] = f[3, 0,  :  ] - 2 * w_a[3] * rho[ 1,:] * d_cs2 * -.3
    f[5, 0,  :  ] = f[6, 0,  :  ] - 2 * w_a[6] * rho[ 1,:] * d_cs2 * -.3
    f[8, 0,  :  ] = f[7, 0,  :  ] - 2 * w_a[7] * rho[ 1,:] * d_cs2 * -.3

    #voutlet
    f[3,-1,  :  ] = f[1,-1,  :  ] - 2 * w_a[1] * rho[-2,:] * d_cs2 * .3
    f[6,-1,  :  ] = f[5,-1,  :  ] - 2 * w_a[5] * rho[-2,:] * d_cs2 * .3
    f[7,-1,  :  ] = f[8,-1,  :  ] - 2 * w_a[8] * rho[-2,:] * d_cs2 * .3

    #poutlet
    #f[3,-1,  :  ] =-f[1,-1,  :  ] + 2 * w_a[1] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )
    #f[6,-1,  :  ] =-f[5,-1,  :  ] + 2 * w_a[5] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )
    #f[7,-1,  :  ] =-f[8,-1,  :  ] + 2 * w_a[8] * rho[-2,:] * (1 + .5*(d_cs4-d_cs2)*(ux[-2,:]-.5*(ux[-2,:]-ux[-3,:]))**2  )

    #bot
    f[2,  :  , 0] = f[4,  :  , 0] 
    f[5,  :  , 0] = f[7,  :  , 0] - 2 * w_a[7] * rho[:, 1] * d_cs2 * -.3
    f[6,  :  , 0] = f[8,  :  , 0] - 2 * w_a[8] * rho[:, 1] * d_cs2 *  .3

    #top
    f[4,  :  ,-1] = f[2,  :  ,-1]  
    f[8,  :  ,-1] = f[6,  :  ,-1] - 2 * w_a[6] * rho[:,-2] * d_cs2 * -.3
    f[7,  :  ,-1] = f[5,  :  ,-1] - 2 * w_a[5] * rho[:,-2] * d_cs2 *  .3
    return(f)

def BC_obstacle(f, r,x_c,y_c):
    #right
    f[1, x_c+r, y_c-r:y_c+r+1 ] = f[3, x_c+r, y_c-r:y_c+r+1 ] 
    f[5, x_c+r, y_c-r:y_c+r+1 ] = f[6, x_c+r, y_c-r:y_c+r+1 ] 
    f[8, x_c+r, y_c-r:y_c+r+1 ] = f[7, x_c+r, y_c-r:y_c+r+1 ] 

    #left
    f[3, x_c-r, y_c-r:y_c+r+1 ] = f[1, x_c-r, y_c-r:y_c+r+1 ] 
    f[6, x_c-r, y_c-r:y_c+r+1 ] = f[5, x_c-r, y_c-r:y_c+r+1 ] 
    f[7, x_c-r, y_c-r:y_c+r+1 ] = f[8, x_c-r, y_c-r:y_c+r+1 ]  

    #top
    f[2, x_c-r:x_c+r+1, y_c+r ] = f[4, x_c-r:x_c+r+1 , y_c+r] 
    f[5, x_c-r:x_c+r+1, y_c+r ] = f[8, x_c-r:x_c+r+1 , y_c+r] 
    f[6, x_c-r:x_c+r+1, y_c+r ] = f[7, x_c-r:x_c+r+1 , y_c+r] 

    #bot
    f[4, x_c-r:x_c+r+1, y_c-r ] = f[2, x_c-r:x_c+r+1 , y_c-r]  
    f[8, x_c-r:x_c+r+1, y_c-r ] = f[5, x_c-r:x_c+r+1 , y_c-r] 
    f[7, x_c-r:x_c+r+1, y_c-r ] = f[6, x_c-r:x_c+r+1 , y_c-r] 

    #centre
    f[0, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001

    f[1, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[2, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[3, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[4, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001

    f[5, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[6, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[7, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    f[8, x_c-r+1:x_c+r, y_c-r+1:y_c+r] = .001
    return(f)

def macro(f, rho, ux, uy ):
    rho[:, :] =  f[0, :, :] + f[1, :, :] + f[2, :, :] + f[3, :, :] + f[4, :, :] + f[5, :, :] + f[6, :, :] + f[7, :, :] + f[8, :, :]
    ux[:, :]  = (f[1, :, :] - f[3, :, :] + f[5, :, :] - f[6, :, :] - f[7, :, :] + f[8, :, :]) / rho[:,:]
    uy[:, :]  = (f[2, :, :] - f[4, :, :] + f[5, :, :] + f[6, :, :] - f[7, :, :] - f[8, :, :]) / rho[:,:]
    return(rho, ux, uy)

def show_vort(ux, uy):
  vort = np.ones((len(ux)-2, len(ux[1])-2))
  vort[:,:] = (ux[1:-1,2:]-ux[1:-1,:-2])/2 - (ux[2:,1:-1]-ux[:-2,1:-1])/2
  #plt.imshow(np.transpose(vort))
  return(vort)

def gif_maker(filenames):
    #temps d'execution
    #start=time.time()
    #pas entre chaque image

    with imageio.get_writer('Couloir.gif', mode='I') as writer:
        i=0
        for filename in filenames:
            i+=1
            print(100*i/(len(filenames)),"% du gif fait")
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(filenames):
        os.remove(filename)


def main():
    Nx    = 450
    Ny    = 150
    lin_x = np.linspace(0,Nx-1,Nx)
    lin_y = np.linspace(0,Ny-1,Ny)
    #print(lin_x)
    Nt    = 4000
    f_eq  = np.ones((9,Nx, Ny))
    #f_eq[1,:30,:]=12
    #print(np.transpose(f_eq[1]))
    f     = np.ones((9,Nx, Ny))
    f_new = np.ones((9,Nx, Ny))

    U0 = 0.3
    ux     = U0*np.ones((Nx, Ny))
    uy     = 0.0*np.ones((Nx, Ny))

    #rho0 = 1
    rho   = np.ones((Nx, Ny))
    #rho[int(Nx/2):] = 2
    #rho = base_wave(rho, rho0)
    #print(np.transpose(rho))
    #plt.imshow(np.transpose(rho))
    #plt.show()
    
    filenames = []

    w_a   = np.array([4/9,     1/9,     1/9,     1/9,     1/9,     1/36,     1/36,     1/36,     1/36])
    c_a   = np.array([[0,0],  [1,0],   [0,1],   [-1,0], [0,-1],   [1,1],    [-1,1],   [-1,-1],  [1,-1]])
    c_s   = 1/np.sqrt(3)
    print("c_s =", c_s, "et Ma =", np.max(np.sqrt(ux[:,:]**2 + uy[:,:]**2))/c_s)
    Tau   = .6
    d_Tau = 1/Tau
    d_cs2 = 1/(c_s**2)
    d_cs4 = 1/(c_s**4)

    x_c, y_c, r = int(.2*Nx), int(.5*Ny), int(.03*Ny)


    #plt.plot(lin_x, rho[:,20], label = "1")
    f, f_eq = init(f, f_eq, rho, ux, uy, w_a, d_cs2, d_cs4)
    f = BC_obstacle(f, r, x_c, y_c) 

    rho, ux, uy = macro(f, rho, ux, uy)
    #plt.plot(lin_x, rho[:,20], label = "2") 
    #plt.legend()
    #plt.show()    
    mass0 = mass_check(rho)
    #plt.imshow(np.transpose(rho[:,:]), vmin = .9)
    #plt.show()
    for t in range(Nt+1):
      #print(t)
      f, f_eq = collision(f, f_eq, rho, ux, uy, w_a, d_cs2, d_cs4, d_Tau)
      f = stream(f, f_new)
      #rho, ux, uy = macro(f, rho, ux, uy)
      #print("stream", 100*(mass_check(rho)-mass0)/mass0,"%")
      #f = BC_driven_channel_vp(f, rho, d_cs2, d_cs4, w_a, ux, uy)
      #f = BC_driven_channel_vv(f, rho, d_cs2, d_cs4, w_a)
      f = BC_driven_channel(f, rho, d_cs2, w_a)
      f = BC_obstacle(f, r, x_c, y_c) 
     # f = BC_driven_perio(f, U0, rho0) 
      #rho, ux, uy = macro(f, rho, ux, uy)
      #print("BC", 100*(mass_check(rho)-mass0)/mass0,"%")
      rho, ux, uy = macro(f, rho, ux, uy)

      if t%20==0:
        print(int(t/Nt*100 - t/Nt*100%1), "% restant, variation masse =",100*(mass_check(rho)-mass0)/mass0,"%")

      if t%40==0 and t>100:
          
        plt.tight_layout()
        print(t)
        #plt.legend()
        
        
        vort = show_vort(ux,uy)
        
        fig, ax = plt.subplots(2, 2, dpi=300)
        ax[0][0].imshow(np.transpose(vort[:,:]))
        ax[0][0].set_xlabel('x', fontsize = 12)
        ax[0][0].set_ylabel('y', fontsize = 12)
        ax[0][0].set_title('Vorticity', fontsize = 14)
        ax[0][0].set_aspect('equal')
        ax[0][0].add_patch(Rectangle((x_c-r, y_c-r), r*2, r*2))
        
        ax[0][1].plot(lin_y, ux[int(len(ux)*.2),:], linewidth = .8)
        ax[0][1].set_xlabel('y', fontsize = 12)
        ax[0][1].set_ylabel('speed', fontsize = 12)
        ax[0][1].set_title('Speed profile', fontsize = 14)
        
        ax[1][0].imshow(np.transpose(rho[:,:]), vmin = .9)
        ax[1][0].set_xlabel('x', fontsize = 12)
        ax[1][0].set_ylabel('y', fontsize = 12)
        ax[1][0].set_title('Density', fontsize = 14)
        ax[1][0].set_aspect('equal')
        ax[1][0].add_patch(Rectangle((x_c-r, y_c-r), r*2, r*2) )
        
        ax[1][1].plot(lin_x, ux[:,75], label = t)
        ax[1][1].set_xlabel('x', fontsize = 12)
        ax[1][1].set_ylabel('speed', fontsize = 12)
        ax[1][1].set_title('Speed profile (streamwise)', fontsize = 14)
        #plt.show()
        filename = f'frame_t{t}.png'
        plt.savefig(filename)
        filenames.append(filename)
        plt.close('all')

    plt.figure(dpi=1200)
    #plt.plot(lin_y, ux[90,:])
    #plt.show()

    print("yo")
    vort = show_vort(ux,uy)
    #plt.imshow(np.transpose(vort[:,:]))

    print("yo")
    #plt.imshow(np.transpose(rho[:,:]), vmin = .9)
    #plt.show()

    print("yo")
    #plt.streamplot(lin_x, lin_y, np.transpose(ux), np.transpose(uy),  color= np.transpose(ux[:,:]**2 + uy[:,:]**2)/2, linewidth=.3, arrowsize=0.01, density = 6, cmap='plasma') #color= np.transpose(ux[:,:]**2 + uy[:,:]**2)/2,

    #plt.show()
    fig, ax = plt.subplots(2, 2, dpi=300)
    ax[0][0].imshow(np.transpose(vort[:,:]))
    ax[0][0].set_xlabel('x', fontsize = 12)
    ax[0][0].set_ylabel('y', fontsize = 12)
    ax[0][0].set_title('Vorticity', fontsize = 14)
    ax[0][0].set_aspect('equal')
    ax[0][0].add_patch(Rectangle((x_c-r, y_c-r), r*2, r*2))
    
    ax[0][1].plot(lin_y, ux[int(len(ux)*.2),:], linewidth = .8)
    ax[0][1].set_xlabel('y', fontsize = 12)
    ax[0][1].set_ylabel('speed', fontsize = 12)
    ax[0][1].set_title('Speed profile', fontsize = 14)
    
    ax[1][0].imshow(np.transpose(rho[:,:]), vmin = .9)
    ax[1][0].set_xlabel('x', fontsize = 12)
    ax[1][0].set_ylabel('y', fontsize = 12)
    ax[1][0].set_title('Density', fontsize = 14)
    ax[1][0].set_aspect('equal')
    ax[1][0].add_patch(Rectangle((x_c-r, y_c-r), r*2, r*2) )
    
    
    
    ax[1][1].streamplot(lin_x, lin_y, np.transpose(ux), np.transpose(uy),  color= np.transpose(ux[:,:]**2 + uy[:,:]**2)/2, linewidth=.3, arrowsize=0.01, density = 6, cmap='plasma') #color= np.transpose(ux[:,:]**2 + uy[:,:]**2)/2,
    ax[1][1].set_xlabel('x', fontsize = 12)
    ax[1][1].set_ylabel('y', fontsize = 12)
    ax[1][1].set_title('Streamlines', fontsize = 14)
    ax[1][1].set_aspect('equal')
    ax[1][1].add_patch(Rectangle((x_c-r, y_c-r), r*2, r*2))
    
    
    
    fig.suptitle('Summary')
    fig.show()
    filename = f'summary.png'
    plt.savefig(filename)
    plt.close
    
    gif_maker(filenames)

    print("yo")
a=np.array([1,2,3,4,5])
print(a)
print(a[3:1:-1])
main()
