//  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each
//  new/modif of public class in gravilib.cpp

#include <iostream>
#include "gravilib.h"

using std::string;


Dimension::Dimension()
{this->hello_text = "Hello World from cpp";}

void Dimension::print_hello_world() const
{
    std::cout << this->hello_text;
}