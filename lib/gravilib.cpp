//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

/* Simulateur_gravi_3D : Un simulateur de gravité simple avec rendu 3D
   Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>. */

#include <iostream>
#include "gravilib.hpp"

using std::string;

//*******
//Dimmension
//*******
Dimension::Dimension(){}

void Dimension::print_hello_world() const
{
    std::cout << "Hello World";
}

//*******
//SimpleSphere (classe de base pour les objets)
//*******
SimpleSphere::SimpleSphere(llco* pos,uli masse,uli rayon,lco* speed)
{this->pos = *pos;
this->masse = masse;
this->rayon = rayon;
this->speed = *speed;}

const void SimpleSphere::gravite_avec(SimpleSphere &instance,const float temps){ //cette function applique de la gravitation uniquement a l'instance argument (multithreading futur)
    instance.gravite_coord(this->pos,this->masse,temps);
}
void SimpleSphere::gravite_coord(const llco &pos,const uli masse,const float temps){
    llco dif={pos[0]-this->pos[0],pos[1]-this->pos[1],pos[2]-this->pos[2]};  //diff pos par pos
    ulli divide=(abs(dif[0])+pow(abs(dif[0]),2)+abs(dif[1])+pow(abs(dif[1]),2)+abs(dif[2])+pow(abs(dif[2]),2))/temps;  //diviseurs = dist^2 + sum (dif) / temps(on remultiplie par les composantes de diff)
    this->speed[0]+=dif[0]/divide;
    this->speed[1]+=dif[1]/divide;
    this->speed[2]+=dif[2]/divide;
}
const bool SimpleSphere::t_collision_avec(SimpleSphere &instance){
    if (not instance.t_colli_rapide(this->posmin,this->posmax))
    {return false;}
    if (instance.t_collision_coord(this->pos,this->rayon)){}
}
const bool SimpleSphere::t_collision_coord(const llco &pos,const uli rayon){
    if (pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)
    <pow(rayon+this->rayon,2)){return true;}
    return false;
}
const bool SimpleSphere::t_colli_rapide(const llco &posmin,const llco &posmax){
    if (this->posmin[0]<posmax[0] && this->posmin[1]<posmax[1] && this->posmin[0]<posmax[1] &&
     this->posmin[0]>posmax[0] && this->posmin[1]>posmax[1] && this->posmin[0]>posmax[1]) //test de collision rectangles
     {return true;}
     return false;
}
