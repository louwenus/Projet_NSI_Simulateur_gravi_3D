//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere{ //classe minimale inutile en elle meme, utilisé comme classe de base de la hiérarchie d'héritage, et donc comme classe d'arguments de fonctions
public:
    //pas de constructeur
    
    virtual ~DummySphere() = default;

    virtual void move(float temps);
    virtual uli gravite_stats(float temps,llco &return_pos) const; // masse (interval,position out)
    virtual void accel(lco accel);   //la masse doit etre multiplié par le temps au préalable (réduction du nombre de calcul)
    virtual bool t_collision_avec(DummySphere *instance,llco &v_force,llco &v_force2);
    virtual bool t_collision_coord(llco pos,uli rayon) const;
    virtual bool t_colli_rapide(llco posmin,llco posmax) const;
    virtual void debug() const;
    

};

class SimpleSphere : public DummySphere {  //sphere basique
public:
    //constructeurs et destructeur
    //SimpleSphere();
    SimpleSphere(lli x,lli y,lli z,uli masse,uli rayon,li vx,li vy,li vz);

    virtual void move(float temps);
    virtual uli gravite_stats(float temps,llco &return_pos) const; // masse (interval,position out)
    virtual void accel(const lco accel);   //vecteur acceleration
    virtual bool t_collision_avec(DummySphere *instance); //les veteurs force sont modifiés si collision, 
    virtual bool t_collision_coord(llco pos,uli rayon) const;
    virtual bool t_colli_rapide(llco posmin,llco posmax) const;
    virtual void debug() const;
protected:
    llco posmin;  //utilisé pour les tests de collision rapide
    llco posmax;  //utilisé pour les tests de collision rapide
    llco pos;
    uli masse;
    uli rayon;
    lco speed;
};

#endif