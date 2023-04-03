//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

#ifndef DIMENSIONS_GENERAL_HEADER
#define DIMENSIONS_GENERAL_HEADER

#include "../typedef.hpp"        //typedef and common stuff
#include "../spheres/sphere.hpp" //so sphere can be used in dims
#include "../external/BS_thread_pool.hpp"  //using the amazing thread pool from https://github.com/bshoshany/thread-pool

/*struct grav_const{
    float temps;
    llco pos;
    uli masse;
    uli sanitize;
    atlco accel;
};*/

class BaseDimension
{
public:
    // constructeurs
    BaseDimension();
    virtual ~BaseDimension();
    // autres
    virtual void gravite_all(float temps);
    virtual void move_all(float temps);
    virtual void add_sphere(DummySphere *instance);
    virtual void debug();
    virtual std::list<PyObject *> detect_collisions();
    virtual const std::list<DummySphere *> get_sph_list();

protected:
    // variables
    std::list<DummySphere *> objets;
    static BS::thread_pool tpool;
};
#endif