//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#include "sphere.hpp"

void DummySphere::move(float temps){return;}
uli DummySphere::gravite_stats(float temps,llco &return_pos) const{return 0;}
void DummySphere::gravite_pour(const llco &pos,uli masse){return;}
bool DummySphere::t_collision_avec(DummySphere &instance){return false;}
bool DummySphere::t_collision_coord(const llco &pos,const uli rayon)const{return false;}
bool DummySphere::t_colli_rapide(const llco &posmin,const llco &posmax)const{return false;}