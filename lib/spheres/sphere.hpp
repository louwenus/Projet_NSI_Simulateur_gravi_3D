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
    virtual bool t_collision_avec(DummySphere *instance) = 0;       // test de collision avec une autre sphere
    virtual bool t_collision_coord(llco pos, uli rayon) const = 0;  // teste rapidement (faux positifs) la collsion
    virtual bool t_colli_rapide(llco posmin, llco posmax) const = 0;// teste mieux la collision
    virtual bool t_colli_nextf(llco pos,uli rayon) const = 0;

    virtual void move() = 0;                                                   // dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual double gravite_stats(llco &return_pos, ulli &sane_min_r, double &range) const = 0; // masse (pos,rayon,range)
    virtual void accel(const lco accel) = 0;                                              // vecteur acceleration
    virtual void debug() const = 0;
    virtual void set_speed(li x,li y,li z) = 0;
    virtual void set_ticktime(const float ticktime) = 0;

    // variable
    PyObject *pyparent;
};

class SimpleSphere : public DummySphere
{ // sphere basique
public:
    // constructeurs et destructeur
    // SimpleSphere();
    SimpleSphere(PyObject *parent, lli x, lli y, lli z, double masse, uli rayon, li vx, li vy, li vz);

    // fonctions pour la collision
    virtual bool t_collision_avec(DummySphere *instance); // test de collision avec une autre sphere
    virtual bool t_collision_coord(llco pos, uli rayon) const;
    virtual bool t_colli_rapide(llco posmin, llco posmax) const;
    virtual bool t_colli_nextf(llco pos,uli rayon) const;

    virtual void move();                                                   // dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    virtual double gravite_stats(llco &return_pos, ulli &sane_min_r, double &range) const; // masse (pos,rayon,range)
    virtual void accel(const lco accel);                                              // vecteur acceleration
    virtual void debug() const;
    virtual void set_speed(li x,li y,li z);
    virtual void set_ticktime(const float ticktime);
    virtual void set_masse(double masse);

    llco pos; // declared public to be easily accessible from cython (and then python)
    uli rayon;
    atlco speed;
    double masse;

protected:
    double masse_time;
    llco posmin; // utilisé pour les tests de collision rapide
    llco posmax; // utilisé pour les tests de collision rapide
    float ticktime;
    double range;   // distance 
};

#endif