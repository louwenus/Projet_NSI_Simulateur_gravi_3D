#ifndef MAINGRAVI_CPP
#define MAINGRAVI_CPP

#include <stdio>
using namespace std;

class Dimension{
public:
    //constructeurs
    Dimension();
    Dimension(string text)
    //acceseurs (devrait tous finir par const)
    void print_hello_world() const;
    string return_hello_world() const;
    //mutateur
    void set_hello_world(string text);
    //autres fonction
private:
    //variables
    string hello_text;
    //fonctions privées
}
#endif
