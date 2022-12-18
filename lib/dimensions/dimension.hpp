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

#ifndef DIMENSIONS_GENERAL_HEADER
#define DIMENSIONS_GENERAL_HEADER

#include "../typedef.hpp"  //typedef and common stuff
#include "../spheres/sphere.hpp"  //so sphere can be used in dims

class BaseDimension{
public:
    //constructeurs
    BaseDimension();
    //acceseurs (devrait tous finir par const)
    void print_hello_world() const;
    virtual void gravite_all(float temps);
    virtual void move_all(float temps);
    //mutateur
    //autres fonction
    //variable publiques (non recomendé)
    
protected:
    //variables
    std::list<DummySphere> objets;
    std::list<DummySphere>::iterator iter;
    std::list<DummySphere>::iterator iter2;
    static std::counting_semaphore<32> semaphore;
    //fonctions privées
};


#endif