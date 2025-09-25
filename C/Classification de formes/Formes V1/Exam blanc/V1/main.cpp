//
//  main.cpp
//  Exam blanc
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include <iostream>
#include "Forme.h"
#include "Cercle.h"
#include "Carre.h"
#include "Rectangle.h"


int main(int argc, const char * argv[]) {

    forme f;
    f.afficher();
    cercle c(17);
    c.afficher();
    carre s(18);
    s.afficher();
    rectangle r(19,20);
    r.afficher();
    
    
    return 0;
}
