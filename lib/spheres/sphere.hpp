//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere{ //classe minimale inutile en elle meme, utilisé comme classe de base de la hiérarchie d'héritage, et donc comme classe d'arguments de fonctions
public:
    //pas de constructeur
    
    virtual ~DummySphere() = default;

    virtual void move(float temps);
    virtual uli gravite_stats(float temps,llco &return_pos) const; // masse (interval,utilisé pour return la pos)
    virtual void gravite_pour(const llco &pos,uli masse);   //la masse doit etre multiplié par le temps au préalable (réduction du nombre de calcul)
    virtual bool t_collision_avec(DummySphere &instance);
    virtual bool t_collision_coord(const llco &pos,uli rayon) const;
    virtual bool t_colli_rapide(const llco &posmin,const llco &posmax) const;
    

};

class SimpleSphere : public DummySphere {  //sphere basique
public:
    //constructeurs et destructeur
    //SimpleSphere();
    SimpleSphere(lli x,lli y,lli z,uli masse,uli rayon,lli vx,lli vy,lli vz);

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