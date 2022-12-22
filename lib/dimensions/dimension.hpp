//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
//  avec chaque modif des classes publiques de gravilib.cpp

#ifndef DIMENSIONS_GENERAL_HEADER
#define DIMENSIONS_GENERAL_HEADER

#include "../typedef.hpp"  //typedef and common stuff
#include "../spheres/sphere.hpp"  //so sphere can be used in dims

class BaseDimension{
public:
    //constructeurs
    BaseDimension();
    //autres
    void print_hello_world() const;
    virtual void gravite_all(float temps);
    virtual void move_all(float temps);
    
protected:
    //variables
    std::list<DummySphere> objets;
    std::list<DummySphere>::iterator iter;
    //fonctions privées
};
#endif