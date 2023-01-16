//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere{ //classe minimale inutile en elle meme, utilisé comme classe de base de la hiérarchie d'héritage, et donc comme classe d'arguments de fonctions
public:
    //pas de constructeur
    
    virtual ~DummySphere() = 0;  //constructeur par default requis pour etre virtuel

    //fonctions pour la collision
    virtual u_short colli_stats(lco &return_speed) = 0; // retourne la dureté entre 1 et 10 000, ansi que la vitesse
    virtual bool t_collision_avec(DummySphere *instance) = 0;  //teste la collsion avec une autre sphere
    virtual bool t_collision_coord(llco pos,uli rayon) const = 0;                           //teste rapidement (faux positifs) la collsion
    virtual bool t_colli_rapide(llco posmin,llco posmax) const = 0;                         //teste mieux la collision
    virtual bool fusion(lco speed,u_short dur,DummySphere *instance) = 0;
    virtual std::array<bool,2> collsion(lco speed,u_short dur) = 0;

    virtual ulli gravite_stats(float temps,llco &return_pos) const = 0; // masse (interval,position out)     obtention des stats de gravitation.  la masse est divisé par le temps
    virtual void accel(lco accel) = 0;   //application d'un vecteur acceleration
    virtual void move(float temps) = 0;    //dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual void debug() const = 0;
    
};

class SimpleSphere : public DummySphere {  //sphere basique
public:
    //constructeurs et destructeur
    //SimpleSphere();
    SimpleSphere(lli x,lli y,lli z,ulli masse,uli rayon,li vx,li vy,li vz,u_short dur);

    //fonctions pour la collision
    virtual u_short colli_stats(lco &return_speed); // retourne la dureté entre 1 et 10 000, ansi que la vitesse
    virtual bool t_collision_avec(DummySphere *instance); //test de collision avec une autre sphere
    virtual bool t_collision_coord(llco pos,uli rayon) const;
    virtual bool t_colli_rapide(llco posmin,llco posmax) const;
    virtual bool fusion(lco speed,u_short dur,DummySphere *instance);  //se charge de fusionner avec une autre sphere (NB:non supporté pour les simple spheres)
    virtual std::array<bool,2> collsion(lco speed,u_short dur);

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
    const u_short dur;  //dureté
};

#endif