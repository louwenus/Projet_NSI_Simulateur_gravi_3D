#include <stdio>
#include "gravilib.h"

using namespace std;


Dimension::Dimension() : hello_text("Hello World from CPP")
{}

Dimension::Dimension(string text) : hello_text(text)
{}

void Dimension::print_hello_world()
{
    print("{}\n",this->hello_text);
}
string Dimension::return_hello_world()
{
    return this->hello_text;
}
void Dimension::set_hello_world(string text)
{
    this->hello_text = text;
}
