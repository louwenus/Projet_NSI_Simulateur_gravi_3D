//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

SimpleSphere::SimpleSphere(PyObject *parent, lli x, lli y, lli z, double masse, lli rayon, li vx, li vy, li vz) :
    pyparent(parent),
    pos{x,y,z},
    rayon((ulli)rayon),
    masse(masse),
    posmin{x-rayon, y-rayon, z-rayon},
    posmax{x+rayon,y+rayon,z+rayon}
{
    this->set_speed(vx,vy,vz);
}

void SimpleSphere::move()
{
    // using Ec=y^2/y*mv^2 with y=lorentz's gamma
    // aka v=c*sqrt(E(2c^2m+E))/(C^2m+n)
    // and vector v = v/e*vector e
    //energie cinétique
    double E=(double)sqrt(energie.x*energie.x+energie.y*energie.y+energie.z*energie.z);
    //vitesse
    double v;
    if (isinf(E)) {
        v=c;
    } else {
        v=c*(double)sqrt(E*(2*c2*masse+E))/(c2*masse+E);
    }
    //vitesse/energie
    double factor=v/E*ticktime;
    pos = {pos.x + (lli)((double)energie.x*factor), pos.y + (lli)((double)energie.y*factor), pos.z + (lli)((double)energie.x*factor)};
    this->posmin = {this->pos.x - (lli)this->rayon, this->pos.y - (lli)this->rayon, this->pos.z - (lli)this->rayon};
    this->posmax = {this->pos.x + (lli)this->rayon, this->pos.y + (lli)this->rayon, this->pos.z + (lli)this->rayon};
}
dbco SimpleSphere::get_speed() const {
    // using Ec=y^2/y*mv^2 with y=lorentz's gamma
    // aka v=c*sqrt(E(2c^2m+E))/(C^2m+n)
    // and vector v = v/e*vector e
    //energie cinétique
    double E=(double)sqrt(energie.x*energie.x+energie.y*energie.y+energie.z*energie.z);
    //vitesse
    double v;
    if (isinf(E)) {
        v=c;
    } else {
        v=c*(double)sqrt(E*(2*c2*masse+E))/(c2*masse+E);
    }
    //vitesse/energie
    double factor=v/E;
    return {(double)energie.x*factor,(double)energie.y*factor,(double)energie.x*factor};
}
// gravitation
double SimpleSphere::gravite_stats(llco &return_pos, ulli &sane_min_r) const
{ // cette function retourne la position et la masse*le temps, utilisé pour faire de la gravitation
    return_pos = this->pos;
    sane_min_r = this->rayon;
    return this->masse;
}
void SimpleSphere::accel(const dbco accel)
{ // cette fonction aplique un vecteur acceleration a la sphere
    this->energie.x.fetch_add(accel.x,std::memory_order_relaxed);
    this->energie.y.fetch_add(accel.y,std::memory_order_relaxed);
    this->energie.z.fetch_add(accel.z,std::memory_order_relaxed);
}

// collision
bool SimpleSphere::t_collision_avec(const SimpleSphere *instance) const
{ // cette fonction teste si cette sphere en collisione une autre
    if (not instance->t_colli_rapide(this->posmin, this->posmax))
    {
        return false;
    }
    if (instance->t_collision_coord(this->pos, this->rayon))
    {   
        return true;
    }
    return false;
}
bool SimpleSphere::t_collision_coord(const llco pos,const ulli rayon) const
{ // cette fonction test exactement la présence ou non d'une collision entre 2 spheres
    if (pow((double)(pos.x - this->pos.x), 2) + pow((double)(pos.y - this->pos.y), 2) + pow((double)(pos.z - this->pos.z), 2) < pow((double)(rayon + this->rayon), 2))
    {
        return true;
    }
    return false;
}
bool SimpleSphere::t_colli_rapide(const llco posmin,const llco posmax) const
{                                                                                                                                                                          // cette fonction teste rapidement (faux positifs) si cette sphere en touche une autre
    return (this->posmin.x<posmax.x &&this->posmin.y<posmax.y &&this->posmin.z<posmax.z &&this->posmax.x> posmin.x &&this->posmax.y> posmin.y &&this->posmax.z> posmin.z); // test de collision rectangles
}
void SimpleSphere::set_speed(li x,li y,li z)
{
    // We store Ec, not speed, so calculating Ec based on target speed
    //square speed
    double v2 = x*x + y*y + z*z;
    //gamma de lorentz
    double e;
    if (v2 >= c2){
        e = 1e300;
    } else {
    double g = 1/(double)sqrt((double)1.0-v2/c2);
    //energie cinetique (formule relativiste)
    e = v2*this->masse*(g*g)/(g+1);
    }
    // ->         ->
    // Ec = (e/v)*v
    double ev=e*(double)sqrt(v2);
    this->energie.x = x*ev;
    this->energie.y = y*ev;
    this->energie.z = z*ev;
}
void SimpleSphere::set_energie(double x,double y,double z){
    energie.x=x;
    energie.y=y;
    energie.z=z;
}
dbco SimpleSphere::get_energie() const{
    return {(double)energie.x,(double)energie.y,(double)energie.z};
}
void SimpleSphere::set_masse(double masse)
{
    this->masse=masse;
}