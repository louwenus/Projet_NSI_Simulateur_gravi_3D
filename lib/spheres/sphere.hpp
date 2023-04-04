//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class DummySphere
{ // classe minimale inutile en elle meme, utilisé comme classe de base de la hiérarchie d'héritage, (définition de l'interface minimale)
public:
    DummySphere(PyObject *parent);
    virtual ~DummySphere(); // constructeur par default requis pour etre virtuel

    // fonctions pour la collision
    virtual bool t_collision_avec(DummySphere *instance) = 0;        // teste la collsion avec une autre sphere
    virtual bool t_collision_coord(llco pos, uli rayon) const = 0;   // teste rapidement (faux positifs) la collsion
    virtual bool t_colli_rapide(llco posmin, llco posmax) const = 0; // teste mieux la collision

    virtual ulli gravite_stats(float temps, llco &return_pos, uli &sane_min_r) const = 0; // masse (interval,position out)     obtention des stats de gravitation.  la masse est divisé par le temps
    virtual void accel(lco accel) = 0;                                                    // application d'un vecteur acceleration
    virtual void move(float temps) = 0;                                                   // dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual void debug() const = 0;

    // variable
    PyObject *pyparent;
};

class SimpleSphere : public DummySphere
{ // sphere basique
public:
    // constructeurs et destructeur
    // SimpleSphere();
    SimpleSphere(PyObject *parent, lli x, lli y, lli z, ulli masse, uli rayon, li vx, li vy, li vz);

    // fonctions pour la collision
    virtual bool t_collision_avec(DummySphere *instance); // test de collision avec une autre sphere
    virtual bool t_collision_coord(llco pos, uli rayon) const;
    virtual bool t_colli_rapide(llco posmin, llco posmax) const;

    virtual void move(float temps);                                                   // dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual ulli gravite_stats(float temps, llco &return_pos, uli &sane_min_r) const; // masse (interval,position out)
    virtual void accel(const lco accel);                                              // vecteur acceleration
    virtual void debug() const;
    virtual void set_speed(lco speed);

    llco pos; // declared public to be easily accessible from cython (and then python)
    uli rayon;
    atlco speed;

protected:
    llco posmin; // utilisé pour les tests de collision rapide
    llco posmax; // utilisé pour les tests de collision rapide
    ulli masse;
};

#endif