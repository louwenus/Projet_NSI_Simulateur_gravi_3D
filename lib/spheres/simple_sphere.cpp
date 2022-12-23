//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

SimpleSphere::SimpleSphere(lli x,lli y,lli z,uli masse,uli rayon,li vx,li vy,li vz)
{   this->pos = {x,y,z};

    this->posmin[0]=x-rayon;
    this->posmin[1]=y-rayon;
    this->posmin[2]=z-rayon;

    this->posmax[0]=x+rayon;
    this->posmax[1]=y+rayon;
    this->posmax[2]=z+rayon;
    
    this->masse = masse;
    this->rayon = rayon;
    this->speed = {vx,vy,vz};
}

void SimpleSphere::move(float temps){
    this->pos[0]+=this->speed[0]*temps;
    this->pos[1]+=this->speed[1]*temps;
    this->pos[2]+=this->speed[2]*temps;

    this->posmin[0]=this->pos[0]-this->rayon;
    this->posmin[1]=this->pos[1]-this->rayon;
    this->posmin[2]=this->pos[2]-this->rayon;

    this->posmax[0]=this->pos[0]+this->rayon;
    this->posmax[1]=this->pos[1]+this->rayon;
    this->posmax[2]=this->pos[2]+this->rayon;
}
//gravitation
uli SimpleSphere::gravite_stats(float temps,llco &return_pos)const{ //cette function applique de la gravitation uniquement a l'instance argument (multithreading futur)
    return_pos=this->pos;
    return this->masse*temps;
}
void SimpleSphere::accel(const lco accel){
    this->speed[0]+=accel[0];
    this->speed[1]+=accel[1];
    this->speed[2]+=accel[2];
}
//collision
bool SimpleSphere::t_collision_avec(DummySphere &instance){
    if (not instance.t_colli_rapide(this->posmin,this->posmax))
    {return false;}
    if (instance.t_collision_coord(this->pos,this->rayon)){return true;}
    return false;
}
bool SimpleSphere::t_collision_coord(const llco &pos,uli rayon)const{
    if (pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)
    <pow(rayon+this->rayon,2)){return true;}
    return false;
}
bool SimpleSphere::t_colli_rapide(const llco &posmin,const llco &posmax)const{
    return (this->posmin[0]<posmax[0] && this->posmin[1]<posmax[1] && this->posmin[0]<posmax[1] &&
     this->posmin[0]>posmax[0] && this->posmin[1]>posmax[1] && this->posmin[0]>posmax[1]); //test de collision rectangles
}