// #  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

#include "dimension.hpp"

BaseDimension::BaseDimension()
{
    this->objets = {};
}
BaseDimension::~BaseDimension() {}

const std::list<DummySphere *> BaseDimension::get_sph_list(){
    return this->objets ;
}

void grav(DummySphere *sphere, grav_const &constants){
    llco temp_co;
    uli sanitize;
    uli masse = sphere->gravite_stats(constants.temps,temp_co,sanitize); // on stock la pos dans temp_co
    temp_co = {temp_co.x-constants.pos.x,temp_co.y-constants.pos.y,temp_co.z-constants.pos.z}; // puis on y mets le vecteur distance
    // divide = distance^2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction
    lli divide = temp_co.x*temp_co.x + temp_co.y*temp_co.y + temp_co.z*temp_co.z;
    //l'étape de "sanitisation" permet de mettre une borne inf a dist^2 égale a sum(rayon)^2 (pour éviter une grav trop forte)
    sanitize+=constants.sanitize;sanitize=sanitize*sanitize;
    if (divide < sanitize) [[unlikely]] 
        {divide=sanitize;}
    divide += (abs(temp_co.x) + abs(temp_co.y) + abs(temp_co.z));
    // on calcule l'accel sur l'element de la boucle interne et  on l'applique
    sphere->accel({(li)(-1*(temp_co.x*constants.masse) / divide), (li)(-1*(temp_co.y*constants.masse) / divide), (li)(-1*(temp_co.z*constants.masse) / divide)});
    //et on renvoie celle sur l'element externe
    return {(li)((temp_co.x*masse) / divide), (li)((temp_co.y*masse) / divide), (li)((temp_co.z*masse) / divide)};
}

void BaseDimension::gravite_all(float temps)
{
    lco accel;
    grav_const constant;
    constant.temps = temps;
    std::list<std::future<lco>> results;

    for (std::list<DummySphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator)
    {   
        constant.accel.x=0;constant.accel.y=0;constant.accel.z=0;
        constant.masse=(*iterator)->gravite_stats(temps,constant.pos,constant.sanitize);// on prend les stats de la sphere pointé par l'iterator, et on les passe a chaque thread
        results.clear();


        for (std::list<DummySphere *>::iterator iterator2 = this->objets.begin(); iterator2!=iterator; ++iterator2)
        {
            results.push_back(
                std::async(std::launch::async, grav, *iterator2,std::ref(constant))
            );
        }
        accel = {0,0,0};                            // accel calculé par partie dans chaques thread, a appliqué a la spère pointé par l'iterateur
        for (std::list<std::future<lco>>::iterator iterator2 = results.begin(); iterator2!=results.end(); ++iterator2){
            lco temp=iterator2->get();
            accel.x+=temp.x;
            accel.y+=temp.y;
            accel.z+=temp.z;
        }
        (*iterator)->accel(accel);
    }
}
void BaseDimension::add_sphere(DummySphere *instance)
{
    //Py_INCREF(instance->pyparent);
    this->objets.push_back(instance);
}
void BaseDimension::move_all(float temps)
{
    for(auto iter=this->objets.begin(); iter!=this->objets.end(); ++iter)
        { (*iter)->move(temps); }
}
std::list<PyObject *> BaseDimension::detect_collisions()
{
    std::list<PyObject *> liste = {};
    std::list<DummySphere *>::iterator iterator = this->objets.begin();
    while (iterator != this->objets.end())
    {
        std::list<DummySphere *>::iterator iterator2 = this->objets.begin();
        while (iterator2 != iterator)
        {
            if ((*iterator)->t_collision_avec(*iterator2))
            {
                liste.push_back((*iterator)->pyparent);
                //Py_DECREF((*iterator)->pyparent);
                liste.push_back((*iterator2)->pyparent);
                //Py_DECREF((*iterator2)->pyparent);
                this->objets.erase(iterator2);
                iterator = this->objets.erase(iterator);
                goto detect_collision_endloop;
            }
            iterator2++;
        }
        iterator++;
    detect_collision_endloop:;
    }
    return liste;
}
void BaseDimension::debug()
{
    std::cout << "Debuging BaseDimension\n";
    for(auto iter=this->objets.begin(); iter!=this->objets.end(); ++iter)
        {(*iter)->debug();}
}