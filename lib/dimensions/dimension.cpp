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

    for (std::list<DummySphere>::iterator iterator = this->objets.begin(); iterator != this->objets.end(); ++iterator){
        atlco accel = {0,0,0};  // accel calculé par partie dans chaques thread, a appliqué a la spère pointé par l'iterateur
        uli masse1 = iterator->gravite_stats(temps,pos1);  //on prend les stats de la sphere pointé par l'iterator, et on les passe a chaque thread


        std::for_each(std::execution::par,this->objets.begin(),iterator,   //pour chaque objets précédents dans la liste, on execule la fonction lambda de manierre parallèle
            [temps,pos1,masse1,&accel,iterator](DummySphere &sphere){      //fonction lambda: [groupe de capture(aka var externe acessible)](args){code}
                llco temp_co;
                uli masse2 = sphere.gravite_stats(temps,temp_co);  //on stock la pos dans temp_co
                temp_co={temp_co[0]-pos1[0],temp_co[1]-pos1[1],temp_co[2]-pos1[2]};  //puis on y mets le vecteur distance
                //divide = distance ^ 2 (force gravi) + sum(abs(composante de temp_co)) car on va remultiplier par ces composante pour la direction
                ulli divide=(abs(temp_co[0])+temp_co[0]*temp_co[0]+abs(temp_co[1])+temp_co[1]*temp_co[1]+abs(temp_co[2])+temp_co[2]*temp_co[2]);
                
                //TODO : Finir le calcul de l'accel, et le passer en somme a accel / sphere.accel
                
        });
        iterator->accel({accel[0],accel[1],accel[2]});  //ugly array reconstruction needed because of atomic type
    }
}
void BaseDimension::move_all(float temps){
    std::for_each(std::execution::par,this->objets.begin(),this->objets.end(),[temps](DummySphere &sphere){sphere.move(temps);});
}
void BaseDimension::print_hello_world() const
{
    std::cout << "Hello World";
} 