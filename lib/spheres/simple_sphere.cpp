#include "sphere.hpp"

SimpleSphere::SimpleSphere(lli x,lli y,lli z,uli masse,uli rayon,lli vx,lli vy,lli vz)
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
void SimpleSphere::gravite_pour(const llco &pos,uli masse){
    llco dif={pos[0]-this->pos[0],pos[1]-this->pos[1],pos[2]-this->pos[2]};  //diff pos par pos
    if (dif == llco{0,0,0}){
        return;
    }
    ulli divide=(abs(dif[0])+pow(dif[0],2)+abs(dif[1])+pow(dif[1],2)+abs(dif[2])+pow(dif[2],2));  //diviseurs = dist^2 + sum (dif) / temps(on remultiplie par les composantes de diff)
    this->speed[0]+=dif[0]*masse/divide;
    this->speed[1]+=dif[1]*masse/divide;
    this->speed[2]+=dif[2]*masse/divide;
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