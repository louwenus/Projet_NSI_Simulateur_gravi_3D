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
const inline static bool is_128_bit = true;
const inline static double c = (double)INT64_MAX;
const inline static double c2 = ((double)INT64_MAX*(double)INT64_MAX);
#else
typedef uint64_t ulli;
typedef int64_t lli;
typedef int32_t li;
typedef uint32_t uli;
const inline static bool is_128_bit = false;
const inline static double c = (double)INT32_MAX;
const inline static double c2 = ((double)INT32_MAX*(double)INT32_MAX);
#endif
struct llco
{
    lli x;
    lli y;
    lli z;
};
struct dbco
{
    double x;
    double y;
    double z;
};
struct atdbco
{
    std::atomic<double> x;
    std::atomic<double> y;
    std::atomic<double> z;
};

#endif