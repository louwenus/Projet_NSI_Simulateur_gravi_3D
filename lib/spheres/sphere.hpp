//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere{ //classe minimale inutile en elle meme, utilisé comme classe de base de la hiérarchie d'héritage, et donc comme classe d'arguments de fonctions
public:
    //pas de constructeur
    
    virtual ~DummySphere() = default;  //constructeur par default requis pour etre virtuel

    //fonctions pour la collision
    virtual u_short colli_stats(lco &return_speed); // retourne la dureté entre 1 et 10 000, ansi que la vitesse
    virtual bool t_collision_avec(DummySphere *instance,llco &v_force,llco &v_force2);  //teste la collsion avec une autre sphere
    virtual bool t_collision_coord(llco pos,uli rayon) const;                           //teste rapidement (faux positifs) la collsion
    virtual bool t_colli_rapide(llco posmin,llco posmax) const;                         //teste mieux la collision

    virtual ulli gravite_stats(float temps,llco &return_pos) const; // masse (interval,position out)     obtention des stats de gravitation.  la masse est divisé par le temps
    virtual void accel(lco accel);   //application d'un vecteur acceleration
    virtual void move(float temps);    //dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual void debug() const;
    
};

class SimpleSphere : public DummySphere {  //sphere basique
public:
    //constructeurs et destructeur
    //SimpleSphere();
    SimpleSphere(lli x,lli y,lli z,ulli masse,uli rayon,li vx,li vy,li vz,u_short durete);

    //fonctions pour la collision
    virtual u_short colli_stats(lco &return_speed); // retourne la dureté entre 1 et 10 000, ansi que la vitesse
    virtual bool t_collision_avec(DummySphere *instance); //test de collision avec une autre sphere
    virtual bool t_collision_coord(llco pos,uli rayon) const;
    virtual bool t_colli_rapide(llco posmin,llco posmax) const;

    virtual void move(float temps);     //dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual ulli gravite_stats(float temps,llco &return_pos) const; // masse (interval,position out)
    virtual void accel(const lco accel);   //vecteur acceleration
    virtual void debug() const;
protected:
    llco posmin;  //utilisé pour les tests de collision rapide
    llco posmax;  //utilisé pour les tests de collision rapide
    llco pos;     //position
    ulli masse;
    uli rayon;
    lco speed;
    const u_short durete;  //dureté
};

#endif