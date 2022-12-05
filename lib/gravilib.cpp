//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

#include <iostream>
#include "gravilib.h"

using std::string;


Dimension::Dimension()
{}

void Dimension::print_hello_world() const
{
    std::cout << "Hello World";
}

SimpleSphere::SimpleSphere(llco* pos,uli* masse,uli* rayon,lco* speed)
{this->pos = *pos;
this->masse = *masse;
this->rayon = *rayon;
this->speed = *speed;}