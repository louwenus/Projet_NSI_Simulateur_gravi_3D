//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

SimpleSphere::SimpleSphere(PyObject *parent, lli x, lli y, lli z, double masse, uli rayon, li vx, li vy, li vz) :
    DummySphere(parent),
    pos{x,y,z},
    rayon(rayon),
    speed{vx,vy,vz},
    masse(masse),
    posmin{x-rayon, y-rayon, z-rayon},
    posmax{x+rayon,y+rayon,z+rayon},
    ticktime{1}
{}

void SimpleSphere::move()
{   
    this->pos.x += (int)(this->speed.x) * this->ticktime;
    this->pos.y += (int)(this->speed.y) * this->ticktime;
    this->pos.z += (int)(this->speed.z) * this->ticktime;

    this->posmin = {this->pos.x - this->rayon, this->pos.y - this->rayon, this->pos.z - this->rayon};
    this->posmax = {this->pos.x + this->rayon, this->pos.y + this->rayon, this->pos.z + this->rayon};
}
// gravitation
double SimpleSphere::gravite_stats(llco &return_pos, ulli &sane_min_r, double &range) const
{ // cette function retourne la position et la masse*le temps, utilisé pour faire de la gravitation
    return_pos = this->pos;
    sane_min_r = this->rayon;
    range = this->range;
    return this->masse_time;
}
void SimpleSphere::accel(const lco accel)
{ // cette fonction aplique un vecteur acceleration a la sphere
    this->speed.x.fetch_add(accel.x,std::memory_order_relaxed);
    this->speed.y.fetch_add(accel.y,std::memory_order_relaxed);
    this->speed.z.fetch_add(accel.z,std::memory_order_relaxed);
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
        postemp.x+=(li)(this->speed.x);
        postemp.y+=(li)(this->speed.y);
        postemp.z+=(li)(this->speed.z);
        if (instance->t_colli_nextf(postemp,this->rayon)){
            return true;
        }
    }
    return false;
}
bool SimpleSphere::t_colli_nextf(llco pos,uli rayon) const {
    if (pow(pos.x - this->pos.x - (li)(this->speed.x), 2) + pow(pos.y - this->pos.y - (li)(this->speed.y), 2) + pow(pos.z - this->pos.z - (li)(this->speed.z), 2) < pow(rayon + this->rayon, 2))
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
void SimpleSphere::set_speed(li x,li y,li z)
{
    this->speed.x = x;
    this->speed.y = y;
    this->speed.z = z;
}
void SimpleSphere::set_ticktime(const float ticktime)
{
    this->ticktime=ticktime;
    this->masse_time=masse*ticktime;
    this->range=this->masse_time;
}

void SimpleSphere::set_masse(double masse)
{
    this->masse=masse;
    this->masse_time=masse*this->ticktime;
    this->range=this->masse_time;
}