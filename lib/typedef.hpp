//  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#ifndef TYPEDEF_GRAVI_CPP
#define TYPEDEF_GRAVI_CPP
// external includes
#include <cmath>
#include <list>
#include <functional>
#include <atomic>
#include <iostream>
#include "Python.h"


#if __SIZEOF_INT128__
typedef __uint128_t ulli;
typedef __int128_t lli;
typedef int64_t li;
typedef uint64_t uli;
const bool is_128_bit = true;
#else
typedef uint64_t ulli;
typedef int64_t lli;
typedef int32_t li;
typedef uint32_t uli;
const bool is_128_bit = false;
#endif

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
struct flco
{
    float x;
    float y;
    float z;
};

#endif