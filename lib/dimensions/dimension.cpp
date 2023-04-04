// #  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

#include "dimension.hpp"

BS::thread_pool BaseDimension::tpool = BS::thread_pool();

BaseDimension::BaseDimension()
{
    this->objets = {};
}
BaseDimension::~BaseDimension() {}

const std::list<DummySphere *> BaseDimension::get_sph_list()
{
    return this->objets;
}

void grav(std::list<DummySphere *>::iterator iterator, const std::list<DummySphere *>::iterator end, const float temps)
{
    /* Cette fonction calcule et applique la gravitation entre la sphère pointé par iterator, et toute les suivante sur cet iterateur jusqu'a end.
    end doit évidement être un itérateur sur le meme objet que iterator, et situé après lui
    temps et la constante de temps passé aux gravite_stats*/
    llco coo;
    DummySphere *sphere = (*iterator);
    uli sanitize;
    uli masse = sphere->gravite_stats(temps, coo, sanitize);
    lco accel = {0, 0, 0};

    llco temp_co;
    uli sanitize2;
    uli masse2;
    lli divide;
    for (; iterator != end; ++iterator)
    {
        masse2 = (*iterator)->gravite_stats(temps, temp_co, sanitize2);      // on stock la pos dans temp_co
        temp_co = {temp_co.x - coo.x, temp_co.y - coo.y, temp_co.z - coo.z}; // puis on y mets le vecteur distance
        // divide = distance^2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction
        divide = temp_co.x * temp_co.x + temp_co.y * temp_co.y + temp_co.z * temp_co.z;
        // l'étape de "sanitisation" permet de mettre une borne inf a dist^2 égale a sum(rayon)^2 (pour éviter une grav trop forte)
        sanitize2 += sanitize;
        sanitize2 = sanitize2 * sanitize2;
        if (divide < sanitize2) [[unlikely]]
        {
            divide = sanitize2;
        }
        divide += (abs(temp_co.x) + abs(temp_co.y) + abs(temp_co.z));
        // on calcule l'accel sur l'element de la boucle interne et  on l'applique
        (*iterator)->accel({(li)(-1 * (temp_co.x * masse) / divide), (li)(-1 * (temp_co.y * masse) / divide), (li)(-1 * (temp_co.z * masse) / divide)});
        // et on calcule celle sur l'element externe
        accel.x += (li)((temp_co.x * masse2) / divide);
        accel.y += (li)((temp_co.y * masse2) / divide);
        accel.z += (li)((temp_co.z * masse2) / divide);
    }
    sphere->accel(accel);
}

void BaseDimension::gravite_all(float temps)
{

    for (std::list<DummySphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator)
    {
        this->tpool.push_task(grav, iterator, this->objets.end(), temps);
    }
    this->tpool.wait_for_tasks();
}
void BaseDimension::add_sphere(DummySphere *instance)
{
    // Py_INCREF(instance->pyparent);
    this->objets.push_back(instance);
}
void BaseDimension::move_all(float temps)
{
    for (auto iter = this->objets.begin(); iter != this->objets.end(); ++iter)
    {
        (*iter)->move(temps);
    }
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
                // Py_DECREF((*iterator)->pyparent);
                liste.push_back((*iterator2)->pyparent);
                // Py_DECREF((*iterator2)->pyparent);
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
    for (auto iter = this->objets.begin(); iter != this->objets.end(); ++iter)
    {
        (*iter)->debug();
    }
}