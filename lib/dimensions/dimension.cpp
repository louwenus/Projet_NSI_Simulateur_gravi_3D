//#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

#include "dimension.hpp"

BaseDimension::BaseDimension() {
    this->objets = {};
}
void BaseDimension::gravite_all(float temps){
    llco pos = {0,0,0};
    for (this->iter = this->objets.begin(); this->iter != this->objets.end(); ++this->iter){
        ulli masse = iter->gravite_stats(temps,pos);
        std::for_each(std::execution::par,this->objets.begin(),this->objets.end(),[pos,masse](DummySphere &sphere){sphere.gravite_pour(pos,masse);});
    }
}
void BaseDimension::move_all(float temps){
    std::for_each(std::execution::par,this->objets.begin(),this->objets.end(),[temps](DummySphere &sphere){sphere.move(temps);});
}
void BaseDimension::print_hello_world() const
{
    std::cout << "Hello World";
} 