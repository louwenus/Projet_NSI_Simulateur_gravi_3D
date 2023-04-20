//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef TYPEDEF_GRAVI_CPP
#define TYPEDEF_GRAVI_CPP
// external includes
#include <cmath>
#include <string>
#include <array>
#include <list>
#include <future>
#include <atomic>
#include <iostream>
#include "Python.h"
// for easier args typing
typedef uint64_t ulli;
typedef int64_t lli;
typedef int32_t li;
typedef uint32_t uli;



struct llco
{
    lli x;
    lli y;
    lli z;
};
struct lco
{
    li x;
    li y;
    li z;
};
struct atlco
{
    std::atomic<li> x;
    std::atomic<li> y;
    std::atomic<li> z;

    operator lco() {return {(li)this->x,(li)this->y,(li)this->z};}
};

#endif