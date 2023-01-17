//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

SimpleSphere::SimpleSphere(lli x,lli y,lli z,ulli masse,uli rayon,li vx,li vy,li vz,u_short dur):dur(dur)  //crée une simple sphere, avec les stats indiqué
{   this->pos = {x,y,z};

    this->posmin={x-rayon,y-rayon,z-rayon};
    this->posmax={x+rayon,y+rayon,z+rayon};
    
    this->masse = masse;
    this->rayon = rayon;
    this->speed = {vx,vy,vz};
}

void SimpleSphere::move(float temps){
    this->pos[0]+=this->speed[0]*temps;
    this->pos[1]+=this->speed[1]*temps;
    this->pos[2]+=this->speed[2]*temps;

    this->posmin={this->pos[0]-this->rayon, this->pos[1]-this->rayon, this->pos[2]-this->rayon};
    this->posmax={this->pos[0]+this->rayon, this->pos[1]+this->rayon, this->pos[2]+this->rayon};
}
//gravitation
ulli SimpleSphere::gravite_stats(float temps,llco &return_pos)const{ //cette function retourne la position et la masse*le temps, utilisé pour faire de la gravitation
    return_pos=this->pos;
    return this->masse*temps;
}
void SimpleSphere::accel(const lco accel){  //cette fonction aplique un vecteur acceleration a la sphere
    this->speed[0]+=accel[0];
    this->speed[1]+=accel[1];
    this->speed[2]+=accel[2];
}

//collision
bool SimpleSphere::t_collision_avec(DummySphere *instance){  //cette fonction teste si cette sphere en collisione une autre
    if (not instance->t_colli_rapide(this->posmin,this->posmax))
    {return false;}
    if (instance->t_collision_coord(this->pos,this->rayon)){return true;}
    return false;
}
bool SimpleSphere::t_collision_coord(llco pos,uli rayon)const{  // cette fonction test exactement la présence ou non d'une collision entre 2 spheres
    if (pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)+pow(pos[0]-this->pos[0],2)
    <pow(rayon+this->rayon,2)){return true;}
    return false;
}
bool SimpleSphere::t_colli_rapide(llco posmin,llco posmax)const{  //cette fonction teste rapidement (faux positifs) si cette sphere en touche une autre
    return (this->posmin[0]<posmax[0] && this->posmin[1]<posmax[1] && this->posmin[0]<posmax[1] &&
     this->posmin[0]>posmax[0] && this->posmin[1]>posmax[1] && this->posmin[0]>posmax[1]); //test de collision rectangles
}
u_short SimpleSphere::colli_stats(lco &return_speed){
    return_speed=this->speed;
    return this->dur;
}
bool SimpleSphere::fusion(lco speed,u_short dur,DummySphere *instance){
    return false; //simple sphere do not support collsion
}
bool SimpleSphere::collsion(lco speed,u_short dur,std::list<DummySphere*> &fragments){
    for (char i=0;i<3;i++){
        this->speed[i]+=((speed[i]-this->speed[i])*dur)/10000;
    }
    return false;
}

void SimpleSphere::debug() const{
    std::cout << "Position:" << this->pos[0] << '/' << this->pos[1] << '/' << this->pos[2] << " Vitesse:" << this->speed[0] << '/' << this->speed[1] << '/'  << this->speed[2] <<'\n' ;
}