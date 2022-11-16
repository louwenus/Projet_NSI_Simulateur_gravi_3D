//  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each
//  new/modif of public class in gravilib.cpp

#ifndef MAINGRAVI_CPP
#define MAINGRAVI_CPP

#include <stdio.h>
#include <string>
using std::string;

class Dimension{
public:
    //constructeurs
    Dimension();
    //acceseurs (devrait tous finir par const)
    void print_hello_world() const;
    //mutateur
    //autres fonction
    //variable publiques (non recomendé)
    string hello_text;
private:
    //variables
    //string hello_text;
    //fonctions privées
};
#endif