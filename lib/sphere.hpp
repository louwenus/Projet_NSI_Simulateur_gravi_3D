#ifndef MAIN_SPHERE_CPP
#define MAIN_SPHERE_CPP
#include "typedef.hpp"
class SimpleSphere : public DummySphere{
public:
    //constructeurs et destructeur
    SimpleSphere();
    SimpleSphere(llco &pos,uli masse,uli rayon,lco &speed);

    virtual void move(float temps);
    virtual void gravite_avec(DummySphere &instance,float temps) const;
    virtual void gravite_coord(const llco &pos,uli masse,float temps);
    virtual bool t_collision_avec(DummySphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
protected:
    llco posmin;  //utilisé pour les tests de collision rapide
    llco posmax;  //utilisé pour les tests de collision rapide
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};


class DummySphere{ //may be used for pending deletion sphere for exemple, and as base class who do nothing
public:
    //constructeurs
    DummySphere();
    
    virtual void move(float temps);
    virtual void gravite_avec(DummySphere &instance,float temps) const;
    virtual void gravite_coord(const llco &pos,uli masse,float temps);
    virtual bool t_collision_avec(DummySphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
    

};

#endif