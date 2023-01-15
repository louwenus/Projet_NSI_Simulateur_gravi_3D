//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

void DummySphere::move(float temps){return;}
ulli DummySphere::gravite_stats(float temps,llco &return_pos) const{return 0;}
void DummySphere::accel(lco accel){return;}

//colisions
bool DummySphere::t_collision_avec(DummySphere *instance,llco &v_force,llco &v_force2){return false;}
bool DummySphere::t_collision_coord(llco pos,const uli rayon)const{return false;}
bool DummySphere::t_colli_rapide(llco posmin,llco posmax)const{return false;}
u_short DummySphere::colli_stats(lco &return_speed){return_speed={0,0,0};return 0;}

void DummySphere::debug() const {std::cout << "this is a dummy sphere\n" ;}