/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * version1.cpp v1
*/

#include <iostream>
#include <cmath>
#include <string>
#include <fstream>
#include "Bouteille.h"
#include "Alcool.h"
#include "Soft.h"
#include "Vin.h"
#include "Eau.h"

#include "Soda.h"
#include "Alcool_fort.h"
using namespace std;

/**
 * Programme principal
*/
main(){
    Bouteille * b1 = new Alcool_fort();
    Bouteille * b2 = new Vin();
    Bouteille * b3 = new Eau();
    Bouteille * b4 = new Soda();

    b1->afficher();
    b2->afficher();
    b3->afficher();
    b4->afficher();

    delete(b1);
    delete(b2);
    delete(b3);
    delete(b4);

}