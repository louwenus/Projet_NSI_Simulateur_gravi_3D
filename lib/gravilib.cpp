//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

#include <iostream>
#include "gravilib.h"

using std::string;


Dimension::Dimension()
{this->hello_text = "Hello World from cpp\n";}

void Dimension::print_hello_world() const
{
    std::cout << this->hello_text;
}

SimpleSphere::SimpleSphere(coord pos,ull masse,ull rayon,coord speed)
{this->pos = pos;
this->masse = masse;
this->rayon = rayon;
this->speed = speed;}


ForceGravitationnelle(masse1, masse2, distance){
    constGravit = 6.6742*pow(10.0,-11);
    force = (constGravit*masse1*masse2)/pow(distance,2);
    return force
}