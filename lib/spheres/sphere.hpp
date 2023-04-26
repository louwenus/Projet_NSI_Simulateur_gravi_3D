//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef SPHERE_GENERAL_HEADER
#define SPHERE_GENERAL_HEADER
#include "../typedef.hpp"
class SimpleSphere
{ // sphere basique
public:
    // constructeurs et destructeur
    // SimpleSphere();
    SimpleSphere(PyObject *parent, lli x, lli y, lli z, double masse, lli rayon, li vx, li vy, li vz);

    // fonctions pour la collision
    bool t_collision_avec(const SimpleSphere *instance) const; // test de collision avec une autre sphere
    bool t_collision_coord(const llco pos,const ulli rayon) const;
    bool t_colli_rapide(const llco posmin,const llco posmax) const;

    void move();                                                   // dit a la sphere de se déplacer comme si temps seconde s'etait écoulé
    double gravite_stats(llco &return_pos, ulli &sane_min_r) const; // masse (pos,rayon)
    void accel(const flco accel);                                              // vecteur acceleration
    void set_speed(li x,li y,li z);
    flco get_speed() const;
    void set_energie(float x,float y,float z);
    flco get_energie() const;
    void set_ticktime(const float ticktime);
    void set_masse(double masse);

    PyObject *pyparent;
    llco pos; // declared public to be easily accessible from cython (and then python)
    ulli rayon;
    atflco energie;
    double masse;
    std::list<SimpleSphere*>::iterator touche;
protected:
    double masse_time;  //utilisé dans gravitation (évite le recalcul de masse * ticktime a chaque intéraction a chaque frame)
    llco posmin; // utilisé pour les tests de collision rapide
    llco posmax; // utilisé pour les tests de collision rapide
    float ticktime;
};

#endif