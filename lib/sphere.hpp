#ifndef MAIN_SPHERE_CPP
#define MAIN_SPHERE_CPP
#include "typedef.hpp"
class SimpleSphere : public DummySphere{
public:
    //constructeurs
    SimpleSphere();
    SimpleSphere(llco* pos,uli masse,uli rayon,lco* speed);

    virtual void gravite_avec(SimpleSphere &instance,const float temps) const;
    virtual void gravite_coord(const llco &pos,const uli masse,const float temps);
    virtual bool t_collision_avec(SimpleSphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
protected:
    llco posmin;
    llco posmax;
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};


class DummySphere{ //may be used for pending deletion sphere for exemple, and as base class who do nothing
public:
    //constructeurs
    DummySphere();

    virtual void gravite_avec(SimpleSphere &instance,const float temps) const;
    virtual void gravite_coord(const llco &pos,const uli masse,const float temps);
    virtual bool t_collision_avec(SimpleSphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
    

};

#endif