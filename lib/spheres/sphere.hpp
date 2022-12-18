#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere{ //may be used for pending deletion sphere for exemple, and as base class who do nothing
public:
    //constructeurs
    DummySphere();
    
    virtual void move(float temps);
    virtual uli gravite_stats(float temps,llco &return_pos) const; // masse (interval,utilisé pour return la pos)
    virtual void gravite_pour(const llco &pos,uli masse);   //la masse doit etre multiplié par le temps au préalable (réduction du nombre de calcul)
    virtual bool t_collision_avec(DummySphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
    

};

class SimpleSphere : public DummySphere {
public:
    //constructeurs et destructeur
    SimpleSphere();
    SimpleSphere(llco &pos,uli masse,uli rayon,lco &speed);

    virtual void move(float temps);
    virtual uli gravite_stats(float temps,llco &return_pos) const; // masse (interval,utilisé pour return la pos)
    virtual void gravite_pour(const llco &pos,uli masse);   //la masse doit etre multiplié par le temps au préalable (réduction du nombre de calcul)
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

#endif