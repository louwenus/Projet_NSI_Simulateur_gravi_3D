//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

#ifndef MAINGRAVI_CPP
#define MAINGRAVI_CPP

#include <stdio.h>
#include <string>
#include <array>
using std::string;

typedef unsigned long long int ulli;
typedef long long int lli;
typedef long int li;
typedef unsigned long int uli;
typedef std::array<lli, 3> llco;
typedef std::array<li, 3> lco;


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
    //string hello_text;
    //fonctions privées
};
class SimpleSphere{
public:
    //constructeurs
    SimpleSphere();
    SimpleSphere(llco* pos,uli* masse,uli* rayon,lco* speed);
    virtual const void gravite_avec(SimpleSphere* instance);
    virtual void gravite_coord(const llco &pos,const uli &masse);
    virtual const bool t_collision_avec(SimpleSphere* instance);
    virtual const bool t_collision_coord(llco* pos,uli rayon);
    virtual const bool t_colli_rapide(llco posmin,llco posmax);
private:
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};

#endif