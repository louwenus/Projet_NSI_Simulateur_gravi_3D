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
#include "gravilib.h"

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

const void SimpleSphere::gravite_avec(SimpleSphere &instance){ //cette function applique de la gravitation uniquement a l'instance argument (multithreading futur)
    instance.gravite_coord(this->pos,this->masse);
}
void SimpleSphere::gravite_coord(const llco &pos,const uli masse){
    llco dif={pos[0]-this->pos[0],pos[1]-this->pos[1],pos[2]-this->pos[2]};  //diff pos par pos
    ulli divide=abs(dif[0])+pow(abs(dif[0]),2)+abs(dif[1])+pow(abs(dif[1]),2)+abs(dif[2])+pow(abs(dif[2]),2);  //diviseurs = dist^2 + sum (dif) (on remultiplie par les composantes de diff)
    this->speed.data()+={dif[0]/divide,dif[1]/divide,dif[2]/divide};
}
const bool SimpleSphere::t_collision_avec(const SimpleSphere* instance){}
const bool SimpleSphere::t_collision_coord(const llco &pos,const uli rayon){}
const bool SimpleSphere::t_colli_rapide(const llco &posmin,const llco &posmax){}
