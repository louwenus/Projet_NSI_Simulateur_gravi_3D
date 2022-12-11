#ifndef MAIN_SPHERE_CPP
#define MAIN_SPHERE_CPP
#include "typedef.hpp"
class SimpleSphere{
public:
    //constructeurs
    SimpleSphere();
    SimpleSphere(llco* pos,uli masse,uli rayon,lco* speed);
    virtual const void gravite_avec(SimpleSphere &instance,const float temps);
    virtual void gravite_coord(const llco &pos,const uli masse,const float temps);
    virtual const bool t_collision_avec(SimpleSphere &instance);
    virtual const bool t_collision_coord(const llco &pos,uli rayon);
    virtual const bool t_colli_rapide(const llco &posmin,const llco &posmax);
private:
    llco posmin;
    llco posmax;
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};

#endif