//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

/* Simulateur_gravi_3D : Un simulateur de gravité simple avec rendu 3D
   Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>. */

#ifndef MAINGRAVI_CPP
#define MAINGRAVI_CPP

#include <cmath>
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
    SimpleSphere(llco* pos,uli masse,uli rayon,lco* speed);
    virtual const void gravite_avec(SimpleSphere &instance);
    virtual void gravite_coord(const llco &pos,const uli masse);
    virtual const bool t_collision_avec(const SimpleSphere* instance);
    virtual const bool t_collision_coord(const llco &pos,uli rayon);
    virtual const bool t_colli_rapide(const llco &posmin,const llco &posmax);
private:
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};

#endif