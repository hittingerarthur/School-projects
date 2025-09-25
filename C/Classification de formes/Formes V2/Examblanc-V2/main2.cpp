//
//  main.cpp
//  Examblanc-V2
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include <iostream>
#include "Forme2.h"
#include "Cercle2.h"
#include "Carre2.h"
#include "Rectangle2.h"


int main(int argc, const char * argv[]) {

    
    cout<<"----------------------------------------------"<<endl;
    cout<<"     Test avec les pointeurs "<<endl;
    cout<<"----------------------------------------------"<<endl;

    forme * f1 = new cercle (17);
    forme * f2 = new carre (18);
    forme * f3 = new rectangle (19,20);

    f1->afficher();
    f2->afficher();
    f3->afficher();

    delete f1;
    delete f2;
    delete f3;
    return 0;
}
