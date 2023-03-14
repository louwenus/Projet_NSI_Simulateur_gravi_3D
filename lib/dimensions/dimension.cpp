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

void BaseDimension::gravite_all(float temps)
{
    llco pos1 = {0, 0, 0}; // pour eviter de recreer une variable a chaque fois

    for (std::list<DummySphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator)
    {
        atllco accel = {0, 0, 0};                             // accel calculé par partie dans chaques thread, a appliqué a la spère pointé par l'iterateur
        uli masse1 = (*iterator)->gravite_stats(temps, pos1); // on prend les stats de la sphere pointé par l'iterator, et on les passe a chaque thread

        std::for_each(std::execution::par, this->objets.begin(), iterator, // pour chaque objets précédents dans la liste, on execule la fonction lambda de manierre parallèle
                      [temps, pos1, masse1, &accel](DummySphere *sphere) { // fonction lambda: [groupe de capture(aka var externe acessible)](args){code}
                          llco temp_co;
                          uli masse2 = sphere->gravite_stats(temps, temp_co);                     // on stock la pos dans temp_co
                          temp_co = {temp_co.x - pos1.x, temp_co.y - pos1.y, temp_co.z - pos1.z}; // puis on y mets le vecteur distance
                          // divide = distance ^ 2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction
                          lli divide = (abs(temp_co.x) + temp_co.x * temp_co.x + abs(temp_co.y) + temp_co.y * temp_co.y + abs(temp_co.z) + temp_co.z * temp_co.z);
                          // on augmente l'accel sur l'element exterieur
                          if (divide != 0)
                          {
                              //std::cout << "masse1:" << masse1 << "masse2:" << masse2 << "divide:" << divide;
                              accel.x += ((temp_co.x * masse2) / divide);
                              accel.y += ((temp_co.y * masse2) / divide);
                              accel.z += ((temp_co.z * masse2) / divide);
                              // on calcule l'accel sur l'element de la boucle interne
                              temp_co.x = -1 * (temp_co.x * masse1) / divide;
                              temp_co.y = -1 * (temp_co.y * masse1) / divide;
                              temp_co.z = -1 * (temp_co.z * masse1) / divide;
                              // qu'on applique
                              sphere->accel({(li)temp_co.x, (li)temp_co.y, (li)temp_co.z});
                          }
                      });
        (*iterator)->accel({(li)accel.x, (li)accel.y, (li)accel.z}); // ugly array reconstruction needed because of atomic type
    }
}
void BaseDimension::add_sphere(DummySphere *instance)
{
    Py_INCREF(instance->pyparent);
    this->objets.push_back(instance);
}
void BaseDimension::move_all(float temps)
{
    std::for_each(std::execution::par, this->objets.begin(), this->objets.end(), [temps](DummySphere *sphere)
                  { sphere->move(temps); });
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
                std::cout << "colision detected\n";
                liste.push_back((*iterator)->pyparent);
                Py_DECREF((*iterator)->pyparent);
                liste.push_back((*iterator2)->pyparent);
                Py_DECREF((*iterator2)->pyparent);
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
    std::for_each(std::execution::seq, this->objets.begin(), this->objets.end(), [](DummySphere *sphere)
                  { sphere->debug(); });
}