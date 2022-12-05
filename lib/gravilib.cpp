//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

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
SimpleSphere::SimpleSphere(llco* pos,uli* masse,uli* rayon,lco* speed)
{this->pos = *pos;
this->masse = *masse;
this->rayon = *rayon;
this->speed = *speed;}

void SimpleSphere::gravite_avec(SimpleSphere* instance){ //cette function applique de la gravitation uniquement a l'instance argument (multithreading futur)
    instance->gravite_coord(&this->pos,this->masse)
}
void SimpleSphere::gravite_coord(llco* pos,uli masse){}
bool SimpleSphere::t_colision_avec(SimpleSphere* instance){}
bool SimpleSphere::t_colision_coord(llco* pos,uli rayon){}
bool SimpleSphere::t_coli_rapide(llco posmin,llco posmax){}