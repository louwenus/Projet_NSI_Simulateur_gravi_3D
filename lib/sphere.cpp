#include "sphere.hpp"

using std::string;

//*******
//SimpleSphere (classe de base pour les objets)
//*******
SimpleSphere::SimpleSphere(llco &pos,uli masse,uli rayon,lco &speed)
{this->pos = pos;
this->masse = masse;
this->rayon = rayon;
this->speed = speed;
}
void SimpleSphere::move(float temps){
    this->pos[0]+=this->speed[0]*temps;
    this->pos[1]+=this->speed[1]*temps;
    this->pos[2]+=this->speed[2]*temps;
}
//gravitation
void SimpleSphere::gravite_avec(DummySphere &instance,float temps)const{ //cette function applique de la gravitation uniquement a l'instance argument (multithreading futur)
    instance.gravite_coord(this->pos,this->masse,temps);
}
void SimpleSphere::gravite_coord(const llco &pos,const uli masse,float temps){
    llco dif={pos[0]-this->pos[0],pos[1]-this->pos[1],pos[2]-this->pos[2]};  //diff pos par pos
    ulli divide=(abs(dif[0])+pow(abs(dif[0]),2)+abs(dif[1])+pow(abs(dif[1]),2)+abs(dif[2])+pow(abs(dif[2]),2))/temps;  //diviseurs = dist^2 + sum (dif) / temps(on remultiplie par les composantes de diff)
    this->speed[0]+=dif[0]/divide;
    this->speed[1]+=dif[1]/divide;
    this->speed[2]+=dif[2]/divide;
}
//collision
bool SimpleSphere::t_collision_avec(DummySphere &instance){
    if (not instance.t_colli_rapide(this->posmin,this->posmax))
    {return false;}
    if (instance.t_collision_coord(this->pos,this->rayon)){}
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
//*******
// Dummy sphere
//*******
void DummySphere::move(float temps){return;}
void DummySphere::gravite_avec(DummySphere &instance,float temps)const{return;}
void DummySphere::gravite_coord(const llco &pos,uli masse,float temps){return;}
bool DummySphere::t_collision_avec(DummySphere &instance){return false;}
bool DummySphere::t_collision_coord(const llco &pos,const uli rayon)const{return false;}
bool DummySphere::t_colli_rapide(const llco &posmin,const llco &posmax)const{return false;}