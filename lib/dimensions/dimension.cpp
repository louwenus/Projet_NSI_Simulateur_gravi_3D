//#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

//  Note: Il faut penser à éditer gravilib.cpp, gravilib.h & gravilb.pyx
//  avec chaque modif des classes publiques de gravilib.cpp

#include "dimension.hpp"

BaseDimension::BaseDimension() {
    this->objets = {};
}
BaseDimension::~BaseDimension(){}

void BaseDimension::gravite_all(float temps){
    llco pos1 = {0,0,0};            //pour eviter de recreer une variable a chaque fois

    for (std::list<DummySphere*>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator){
        atlco accel = {0,0,0};  // accel calculé par partie dans chaques thread, a appliqué a la spère pointé par l'iterateur
        uli masse1 = (*iterator)->gravite_stats(temps,pos1);  //on prend les stats de la sphere pointé par l'iterator, et on les passe a chaque thread


        std::for_each(std::execution::par,this->objets.begin(),iterator,   //pour chaque objets précédents dans la liste, on execule la fonction lambda de manierre parallèle
            [temps,pos1,masse1,&accel,iterator](DummySphere* sphere){      //fonction lambda: [groupe de capture(aka var externe acessible)](args){code}
                llco temp_co;
                uli masse2 = sphere->gravite_stats(temps,temp_co);  //on stock la pos dans temp_co
                temp_co={temp_co[0]-pos1[0],temp_co[1]-pos1[1],temp_co[2]-pos1[2]};  //puis on y mets le vecteur distance
                //divide = distance ^ 2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction
                lli divide=(abs(temp_co[0])+temp_co[0]*temp_co[0]+abs(temp_co[1])+temp_co[1]*temp_co[1]+abs(temp_co[2])+temp_co[2]*temp_co[2]);
                //on augmente l'accel sur l'element exterieur
                if (divide!=0){
                std::cout << "masse1:" << masse1 << "masse2:" << masse2 << "divide:" << divide ;
                accel[0]+=((temp_co[0]*masse2)/divide);
                accel[1]+=((temp_co[1]*masse2)/divide);
                accel[2]+=((temp_co[2]*masse2)/divide);
                //on calcule l'accel sur l'element de la boucle interne
                temp_co[0]= -1*(temp_co[0]*masse1)/divide;
                temp_co[1]= -1*(temp_co[1]*masse1)/divide;
                temp_co[2]= -1*(temp_co[2]*masse1)/divide;
                //qu'on applique
                sphere->accel({(li)temp_co[0],(li)temp_co[1],(li)temp_co[2]});}
        });
        (*iterator)->accel({(li)accel[0],(li)accel[1],(li)accel[2]});  //ugly array reconstruction needed because of atomic type
    }
}
void BaseDimension::add_sphere(DummySphere *instance){
    this->objets.push_back(instance);
}
void BaseDimension::move_all(float temps){
    std::for_each(std::execution::par,this->objets.begin(),this->objets.end(),[temps](DummySphere* sphere){sphere->move(temps);});
}
std::list<std::array<PyObject*,2>> BaseDimension::detect_collisions(){
    std::list<std::array<PyObject*,2>> liste = {};
    std::list<DummySphere*>::iterator iterator = this->objets.begin();
    while( iterator != this->objets.end()){
        std::list<DummySphere*>::iterator iterator2 = iterator;
        while (iterator2 != this->objets.end()){
            if ((*iterator)->t_collision_avec(*iterator2)){
                liste.push_back(std::array<PyObject*,2> {(*iterator)->pyparent,(*iterator2)->pyparent});
                this->objets.erase(iterator2);
                iterator=this->objets.erase(iterator);
                goto detect_collsion_endloop;
            }
            iterator2 ++;
        }
        iterator ++;
        detect_collsion_endloop:;
    }
    return liste;
}
void BaseDimension::debug(){
    std::cout << "Debuging BaseDimension\n" ;
    std::for_each(std::execution::seq,this->objets.begin(),this->objets.end(),[](DummySphere* sphere){sphere->debug();});
}