#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each
#  new/modif of public class in gravilib.cpp

#include <stdio>
#include "gravilib.h"

using namespace std;


Dimension::Dimension() : hello_text("Hello World from CPP")
{}

Dimension::Dimension(string text) : hello_text(text)
{}

void Dimension::print_hello_world() const
{
    print("{}\n",this->hello_text);
}
string Dimension::return_hello_world() const
{
    return this->hello_text;
}
void Dimension::set_hello_world(string text)
{
    this->hello_text = text;
}
