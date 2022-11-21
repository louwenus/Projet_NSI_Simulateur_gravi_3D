//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp
// et à ne pas faire de fautes d'ortographes

#include <iostream>
#include "gravilib.h"

using std::string;


Dimension::Dimension()
{this->hello_text = "Hello World from cpp";}

void Dimension::print_hello_world() const
{
    std::cout << this->hello_text;
}
