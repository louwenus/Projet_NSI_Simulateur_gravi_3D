//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

/*  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx
    avec chaque modification des classes publiques de gravilib.cpp */ 

#ifndef DIMENSIONS_GENERAL_HEADER
#define DIMENSIONS_GENERAL_HEADER

#include "../typedef.hpp"                 //typedef and common stuff
#include "../spheres/sphere.hpp"          //Pour que les sphères puissent etre utiliser dans les dims
#include "../external/BS_thread_pool.hpp" //utilisation des thread pool de https://github.com/bshoshany/thread-pool

class BaseDimension

{
public:
    // Méthode constructeurs
    BaseDimension();
    virtual ~BaseDimension();
    // Autre méthodes
    virtual void gravite_all();
    virtual void move_all();
    virtual void add_sphere(DummySphere *instance);
    virtual std::list<PyObject*> detect_collisions();
    virtual const std::list<DummySphere *> get_sph_list() const;

protected:
    // Variables
    std::list<DummySphere *> objets;
    static BS::thread_pool tpool;
};
#endif