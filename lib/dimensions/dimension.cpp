// #  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

/*  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
    avec chaque modification des classes publiques de gravilib.cpp */

#include "dimension.hpp" //importation des scripts dans dimension.hpp
#include "chrono"

float ticktime=1;

BS::thread_pool BaseDimension::tpool = BS::thread_pool();

BaseDimension::BaseDimension(): objets() {}
BaseDimension::~BaseDimension() {}

const std::list<SimpleSphere *> BaseDimension::get_sph_list() const
{
    return this->objets;
}

void grav(std::list<SimpleSphere *>::iterator iterator, const std::list<SimpleSphere *>::iterator end)
{
    /* Cette fonction calcule et applique la gravitation entre la sphère pointée par iterator, et toute les suivante sur cet iterateur jusqu'à end.
    end doit évidement être un itérateur sur le meme objet que iterator, et situé après lui. temps et la constante de temps passé aux gravite_stats. */

    llco coo;
    SimpleSphere* sphere = (*iterator++);
    ulli sanitize;
    double masse = sphere->gravite_stats(coo, sanitize);
    dbco accel = {0, 0, 0};

    llco coo2;
    dbco temp_co;
    ulli sanitize2;
    double masse2;
    double divide;
    for (; iterator != end; ++iterator)
    {
        masse2 = (*iterator)->gravite_stats(coo2, sanitize2);      // on stock la pos dans temp_co
        temp_co = {(double)(coo2.x - coo.x), (double)(coo2.y - coo.y), (double)(coo2.z - coo.z)}; // puis on y mets le vecteur distance
        // divide = distance^2
        divide = temp_co.x * temp_co.x + temp_co.y * temp_co.y + temp_co.z * temp_co.z;
        // l'étape de "sanitisation" permet de mettre une borne inf à dist^2 égale à sum(rayon)^2 (pour éviter une gravitée trop forte sur deux objets très proches)
        sanitize2 += sanitize;
        sanitize2 = sanitize2 * sanitize2;
        if (divide < sanitize2) [[unlikely]]
        {
            divide = sanitize2;
        }
        double factor = masse*masse2*ticktime/(divide*(double)sqrt(divide));
        // on calcule l'accélération sur l'élément de la boucle interne et  on l'applique
        temp_co.x=factor*temp_co.x;
        temp_co.y=factor*temp_co.y;
        temp_co.z=factor*temp_co.z;

        accel.x += temp_co.x;
        accel.y += temp_co.y;
        accel.z += temp_co.z;

        (*iterator)->accel({-1.0*temp_co.x, -1.0 *temp_co.y, -1.0*temp_co.z });
    }
    sphere->accel(accel);
}

void BaseDimension::gravite_all()
{

    for (std::list<SimpleSphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator)
    {
        this->tpool.push_task(grav, iterator, this->objets.end());
    }
    this->tpool.wait_for_tasks();
}
void BaseDimension::add_sphere(SimpleSphere *instance)
{
    // Py_INCREF(instance->pyparent);
    instance->touche=this->objets.end();
    this->objets.push_back(instance);
}
void BaseDimension::move_all()
{
    for (auto iter = this->objets.begin(); iter != this->objets.end(); ++iter)
    {
        (*iter)->move();
    }
}
void detect_internal(std::list<SimpleSphere *>::reverse_iterator iterator, const std::list<SimpleSphere *>::reverse_iterator end)
{
    SimpleSphere* sphere = (*iterator++);
    while ( iterator != end)
    {
        if (sphere->t_collision_avec(*iterator)){
            sphere->touche=(++iterator).base();
            return;
        }
        ++iterator;
    }
}

std::list<PyObject*> BaseDimension::detect_collisions() {
    for (std::list<SimpleSphere*>::reverse_iterator iterator = this->objets.rbegin(); iterator != this->objets.rend();++iterator)
    {
        this->tpool.push_task(detect_internal, iterator, this->objets.rend());
    }
    this->tpool.wait_for_tasks();
    
    for (std::list<SimpleSphere*>::iterator iterator = this->objets.begin(); iterator != this->objets.end();++iterator){
        SimpleSphere* sphere = (*iterator);
        if (sphere->touche != this->objets.end()){
            (*(sphere->touche))->touche=iterator;
            sphere->touche=this->objets.end();
        }
    }

    std::list<PyObject*> liste = {};

    for (std::list<SimpleSphere *>::iterator iterator = this->objets.begin(); iterator != this->objets.end();){
        SimpleSphere* sph = (*iterator);
        if (sph->touche!=this->objets.end())
        {   
            auto iter2=sph->touche;
            liste.push_back(sph->pyparent);
            liste.push_back((*iter2)->pyparent);

            this->objets.erase(iter2);
            iterator = this->objets.erase(iterator);
        }else {
            ++iterator;
        }
    }
    
    return liste;
}