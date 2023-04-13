//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

SimpleSphere::SimpleSphere(PyObject *parent, lli x, lli y, lli z, ulli masse, uli rayon, li vx, li vy, li vz) :
    DummySphere(parent),
    pos{x,y,z},
    rayon(rayon),
    speed{vx,vy,vz},
    masse(masse),
    posmin{x-rayon, y-rayon, z-rayon},
    posmax{x+rayon,y+rayon,z+rayon}
{}

void SimpleSphere::move(float temps)
{
    this->pos.x += this->speed.x * temps;
    this->pos.y += this->speed.y * temps;
    this->pos.z += this->speed.z * temps;

    this->posmin = {this->pos.x - this->rayon, this->pos.y - this->rayon, this->pos.z - this->rayon};
    this->posmax = {this->pos.x + this->rayon, this->pos.y + this->rayon, this->pos.z + this->rayon};
}
// gravitation
ulli SimpleSphere::gravite_stats(float temps, llco &return_pos, ulli &sane_min_r) const
{ // cette function retourne la position et la masse*le temps, utilisé pour faire de la gravitation
    return_pos = this->pos;
    sane_min_r = this->rayon;
    return this->masse * temps;
}
void SimpleSphere::accel(const lco accel)
{ // cette fonction aplique un vecteur acceleration a la sphere
    this->speed.x += accel.x;
    this->speed.y += accel.y;
    this->speed.z += accel.z;
}

// collision
bool SimpleSphere::t_collision_avec(DummySphere *instance)
{ // cette fonction teste si cette sphere en collisione une autre
    if (not instance->t_colli_rapide(this->posmin, this->posmax))
    {
        return false;
    }
    if (instance->t_collision_coord(this->pos, this->rayon))
    {   
        llco postemp=this->pos;
        postemp.x+=this->speed.x;
        postemp.y+=this->speed.y;
        postemp.z+=this->speed.z;
        if (instance->t_colli_nextf(postemp,this->rayon)){
            return true;
        }
    }
    return false;
}
bool SimpleSphere::t_colli_nextf(llco pos,uli rayon) const {
    if (pow(pos.x - this->pos.x - this->speed.x, 2) + pow(pos.y - this->pos.y - this->speed.y, 2) + pow(pos.z - this->pos.z - this->speed.z, 2) < pow(rayon + this->rayon, 2))
    {
        return true;
    }
    return false;
} 
bool SimpleSphere::t_collision_coord(llco pos, uli rayon) const
{ // cette fonction test exactement la présence ou non d'une collision entre 2 spheres
    if (pow(pos.x - this->pos.x, 2) + pow(pos.y - this->pos.y, 2) + pow(pos.z - this->pos.z, 2) < pow(rayon + this->rayon, 2))
    {
        return true;
    }
    return false;
}
bool SimpleSphere::t_colli_rapide(llco posmin, llco posmax) const
{                                                                                                                                                                          // cette fonction teste rapidement (faux positifs) si cette sphere en touche une autre
    return (this->posmin.x<posmax.x &&this->posmin.y<posmax.y &&this->posmin.z<posmax.z &&this->posmax.x> posmin.x &&this->posmax.y> posmin.y &&this->posmax.z> posmin.z); // test de collision rectangles
}

void SimpleSphere::debug() const
{
    std::cout << "Position:" << this->pos.x << '/' << this->pos.y << '/' << this->pos.z << " Vitesse:" << this->speed.x << '/' << this->speed.y << '/' << this->speed.z << '\n';
}
void SimpleSphere::set_speed(li x,li y,li z)
{
    this->speed.x = x;
    this->speed.y = y;
    this->speed.z = z;
}