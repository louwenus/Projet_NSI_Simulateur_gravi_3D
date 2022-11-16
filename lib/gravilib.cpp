//  Note: Il faut penser a editer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classe publique de gravilib.cpp

#include <iostream>
#include "gravilib.h"

using std::string;


Dimension::Dimension()
{this->hello_text = "Hello World from cpp";}

void Dimension::print_hello_world() const
{
    std::cout << this->hello_text;
}