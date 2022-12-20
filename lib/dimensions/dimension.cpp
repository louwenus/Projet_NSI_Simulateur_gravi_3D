//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
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


#include "dimension.hpp"

using std::string;
//*******
//Dimmension
//*******
//std::counting_semaphore<MAX_THREAD_NUMBER> BaseDimension::semaphore(0);
BaseDimension::BaseDimension() {
    this->objets = {};
}
void BaseDimension::gravite_all(float temps){
    llco pos = {0,0,0};
    for (this->iter = this->objets.begin(); this->iter != this->objets.end(); ++this->iter){
        ulli masse = iter->gravite_stats(temps,pos);
        std::for_each(std::execution::par,this->objets.begin(),this->objets.end(),[pos,masse](DummySphere &sphere){sphere.gravite_pour(pos,masse);});
    }
}


void BaseDimension::print_hello_world() const
{
    std::cout << "Hello World";
} 