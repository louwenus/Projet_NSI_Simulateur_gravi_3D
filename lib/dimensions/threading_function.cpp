# include "dimension.hpp"

void gravite_thread(ulli masse,const llco &position,DummySphere *sphere  ){  //,std::counting_semaphore<MAX_THREAD_NUMBER> &semaphore){
    sphere->gravite_pour(position,masse);
    //semaphore.release();
}
void test(ulli masse, llco &pos,std::counting_semaphore<MAX_THREAD_NUMBER> &semaphore){
    std::cout << "test";
    semaphore.release();
}
