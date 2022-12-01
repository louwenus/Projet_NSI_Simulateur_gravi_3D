//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

#ifndef MAINGRAVI_CPP
#define MAINGRAVI_CPP

#include <stdio.h>
#include <string>
using std::string;

typedef unsigned long long ull;
typedef long long ll;
typedef ll coord[3];


class Dimension{
public:
    //constructeurs
    Dimension();
    //acceseurs (devrait tous finir par const)
    void print_hello_world() const;
    //mutateur
    //autres fonction
    //variable publiques (non recomendé)
    
private:
    //variables
    string hello_text;
    //fonctions privées
};
class SimpleSphere{
public:
    //constructeurs
    SimpleSphere();
    SimpleSphere(coord pos,ull masse,ull rayon,coord speed);
    void gravite_on(coord pos,ull masse);
private:
    coord pos;
    ull masse;
    ull rayon;
    coord speed;
};
#endif