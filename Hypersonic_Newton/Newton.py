# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 10:47:13 2024

@author: p126087
"""
import numpy as np


def read_vect(line):
    if line[2:7] != "facet":
        print("not right line\n")
        return []
    x_txt = ""
    y_txt = ""
    z_txt = ""
    i, i0 = 15, 15
    while line[i]!=' ':
        i+=1
    x_txt = line[i0:i]
    #print(x_txt)
    
    
    i += 1
    i0=i
    while line[i]!=' ':
        i+=1
    y_txt = line[i0:i]
    #print(y_txt)
    
    i += 1
    i0 = i
    z_txt = line[i0:]
    #print(z_txt)
    
    x = float(x_txt)
    y = float(y_txt)
    z = float(z_txt)
    
    return [x, y, z]

def read_point(line):
    if line[6:12] != "vertex":
        print("not right line\n")
        return []
    x_txt = ""
    y_txt = ""
    z_txt = ""
    i, i0 = 13, 13
    while line[i]!=' ':
        i+=1
    x_txt = line[i0:i]
    #print(x_txt)
    
    
    i += 1
    i0=i
    while line[i]!=' ':
        i+=1
    y_txt = line[i0:i]
    #print(y_txt)
    
    i += 1
    i0 = i
    z_txt = line[i0:]
   # print(z_txt)
    
    x = float(x_txt)
    y = float(y_txt)
    z = float(z_txt)
    
    return [x, y, z]

def calc_area(A, B, C):
    scale = 0.001
    xAB, yAB, zAB = abs(A[0]-B[0])*scale, abs(A[1]-B[1])*scale, abs(A[2]-B[2])*scale
    xAC, yAC, zAC = abs(A[0]-C[0])*scale, abs(A[1]-C[1])*scale, abs(A[2]-C[2])*scale    
    return .5 * np.sqrt (   (yAB*zAC - zAB*yAC)**2 + (zAB*xAC - xAB*zAC)**2 +(xAB*yAC - yAB*xAC)**2    )

def calc__projected_areas(face_info):
    Sx, Sy, Sz , St = 0, 0, 0, 0
    for i in range(len(face_info)):
        Sx += abs(face_info[i][0][0] *  face_info[i][1])
        #print(face_info[i][0][0], " * ", face_info[i][1])
        Sy += abs(face_info[i][0][1] *  face_info[i][1])
        Sz += abs(face_info[i][0][2] *  face_info[i][1])
        St += face_info[i][1]
    print("surfaces :",Sx, Sy, Sz, St)
    return Sx, Sy, Sz

def build_face_info(filename, debug = "n"):
    file3D = open(filename, 'r')
   
    face_info = []
    
    a = 0
    line = file3D.readline()
    # print(line)
    if debug == "y":
       print("starting first while")
    while line[2:7] != "facet" and a<30:
        a+=1
        line = file3D.readline()
        #print(a, line)
    face_counter = 0
    face_tot = 0
    if debug == "y":
       print("starting second while")
    while line[0:8] != "endsolid":
        dir_line = read_vect(line)
        if dir_line == []:
            file3D.close()
            return(1)
        if dir_line[0]<0:
            if dir_line[0] == 0.01178855:
                print('hey')
                
            line = file3D.readline()
            line = file3D.readline()
            p1 = read_point(line)
            if p1 == []:
                file3D.close()
                return(1)
            line = file3D.readline()
            p2 = read_point(line)
            if p2 == []:
                file3D.close()
                return(1)
            line = file3D.readline()
            p3 = read_point(line)
            if p3 == []:
                file3D.close()
                return(1)
            area = calc_area(p1, p2, p3)
            #print(area)
            face_info.append([dir_line, area])
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
                
            face_counter += 1
        else:
            #print(dir_line[0])
            if dir_line[0] == 0.01178855:
                print('hey')
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
            line = file3D.readline()
        face_tot +=1
                
    #print(face_info)
    #print(len(face_info))
    print(face_counter, face_tot)
    
    #file3D.close()
    return(face_info)

def build_Cp(face_info):
    AoA = np.ones(len(face_info))
    
    for i in range(len(face_info)):
        vect = face_info[i][0]
        angle = np.arccos(np.clip(np.dot((1, 0, 0),vect), -1, 1))
        if angle<np.pi/2 or angle>3*np.pi/2 :
            print("Error for some angles")
        AoA[i] = angle - np.pi/2
        
        #print(AoA[i])
    Cp = 2*np.sin(AoA)
    return(AoA, Cp)
        
def build_total_force(Cp, face_info, rho, v0):
    Fx, Fy, Fz = 0, 0, 0
    Sx, Sy, Sz = calc__projected_areas(face_info)
    print("Les surfaces sont: ", Sx, Sy, Sz)
    
    for i in range(len(Cp)):
        #print("Fx +=", face_info[i][0][0],"*", Cp[i],"*", .5*rho*v0**2)
        Fx += -face_info[i][0][0]*Cp[i] *.5*rho*v0**2 * face_info[i][1]
        Fy += -face_info[i][0][1]*Cp[i] *.5*rho*v0**2 * face_info[i][1]
        Fz += -face_info[i][0][2]*Cp[i] *.5*rho*v0**2 * face_info[i][1]
    
    Cd =  Fx / (.5 * rho * v0**2 * Sx)
    Cy =  Fy / (.5 * rho * v0**2 * Sy)
    Cl =  Fz / (.5 * rho * v0**2 * Sz)
    return(Fx, Fy, Fz, Cd, Cy, Cl)
    
def main():
    V_inf = 100 #m/s
    rho = 1 # Kg/m3
    #stl_file = "BDY_VEH_1.stl" # file containing the stl of the studied geometry
    stl_file = "1250_polygon_sphere_100mm.STL"
    #stl_file = "5000_polygon_sphere_100mm.STL"
   
    # creates a list containg the normal vector and area of each cell
    face_info = build_face_info(stl_file)
    if face_info == 1:
        return 1
    print(len(face_info))
    #creates two lists, one containg the angle of attack of each face (useless so far) and one contain the addimensional pressure coefficient of each face
    AoA, Cp = build_Cp(face_info)
    #print(Cp)
    Fx, Fy, Fz, Cd, Cy, Cl= build_total_force(Cp, face_info, rho, V_inf)
    print("Force de trainée :" ,Fx, "\nForce latérale :", Fy,"\nForce de portance :", Fz)
    print("Coefficient de trainée :", Cd, "\nCoefficient latéral :", Cy,"\nCoefficient de portance :", Cl)
    
#test1 =  "  facet normal 0.616703373 0.0779415822 -0.783327555"

#test2 = "      vertex 3001.65942 191.815247 867.048706"

#read_vect(test1)
#read_point(test2)

main()