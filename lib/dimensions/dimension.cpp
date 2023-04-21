// #  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

/*  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
    avec chaque modification des classes publiques de gravilib.cpp */

#include "dimension.hpp" //importation des scripts dans dimension.hpp
#include "chrono"
BS::thread_pool BaseDimension::tpool = BS::thread_pool();

BaseDimension::BaseDimension(): objets() {}
BaseDimension::~BaseDimension() {}

const std::list<DummySphere *> BaseDimension::get_sph_list() const
{
    return this->objets;
}

void grav(std::list<DummySphere *>::iterator iterator, const std::list<DummySphere *>::iterator end)
{
    /* Cette fonction calcule et applique la gravitation entre la sphère pointée par iterator, et toute les suivante sur cet iterateur jusqu'à end.
    end doit évidement être un itérateur sur le meme objet que iterator, et situé après lui. temps et la constante de temps passé aux gravite_stats. */

    llco coo;
    DummySphere *sphere = (*iterator++);
    ulli sanitize;
    double range1;
    double masse = sphere->gravite_stats(coo, sanitize, range1);
    lco accel = {0, 0, 0};

    llco temp_co;
    double range2;
    ulli sanitize2;
    double masse2;
    double divide;
    for (; iterator != end; ++iterator)
    {
        masse2 = (*iterator)->gravite_stats(temp_co, sanitize2, range2);      // on stock la pos dans temp_co
        temp_co = {temp_co.x - coo.x, temp_co.y - coo.y, temp_co.z - coo.z}; // puis on y mets le vecteur distance
        // divide = distance^2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction (optimisation)
        divide = temp_co.x * temp_co.x + temp_co.y * temp_co.y + temp_co.z * temp_co.z;
        // l'étape de "sanitisation" permet de mettre une borne inf à dist^2 égale à sum(rayon)^2 (pour éviter une gravitée trop forte)
        sanitize2 += sanitize;
        sanitize2 = sanitize2 * sanitize2;
        if (divide < sanitize2) [[unlikely]]
        {
            divide = sanitize2;
        }
        if (divide < range1)
        {
            divide += (abs(temp_co.x) + abs(temp_co.y) + abs(temp_co.z));
            if (divide < range1 and divide < range2)
            {
                // on calcule l'accélération sur l'élément de la boucle interne et  on l'applique
                (*iterator)->accel({(li)(-1 * (masse * temp_co.x) / divide), (li)(-1 * (masse * temp_co.y) / divide), (li)(-1 * (masse * temp_co.z) / divide)});
                // Enfin on calcule celle sur l'élément externe
                accel.x += (li)((temp_co.x * masse2) / divide);
                accel.y += (li)((temp_co.y * masse2) / divide);
                accel.z += (li)((temp_co.z * masse2) / divide);
            } else {
                (*iterator)->accel({(li)(-1 * (masse * temp_co.x) / divide), (li)(-1 * (masse * temp_co.y) / divide), (li)(-1 * (masse * temp_co.z) / divide)});
            }
            
        } else if (divide < range2)
        {
            divide += (abs(temp_co.x) + abs(temp_co.y) + abs(temp_co.z));
            accel.x += (li)((masse2 * temp_co.x) / divide);
            accel.y += (li)((masse2 * temp_co.y) / divide);
            accel.z += (li)((masse2 * temp_co.z) / divide);
        }
    }
    sphere->accel(accel);
}

void BaseDimension::gravite_all()
{

    for (std::list<DummySphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator)
    {
        this->tpool.push_task(grav, iterator, this->objets.end());
    }
    this->tpool.wait_for_tasks();
}
void BaseDimension::add_sphere(DummySphere *instance)
{
    // Py_INCREF(instance->pyparent);
    this->objets.push_back(instance);
}
void BaseDimension::move_all()
{
    for (auto iter = this->objets.begin(); iter != this->objets.end(); ++iter)
    {
        (*iter)->move();
    }
}
std::list<PyObject *> BaseDimension::detect_collisions()
{
    auto start = std::chrono::high_resolution_clock::now();
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
            ++iterator2;
        }
        ++iterator;
    detect_collision_endloop:;
    }
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);
    std::cout << "detection time in ms:" << duration.count();
    return liste;
}