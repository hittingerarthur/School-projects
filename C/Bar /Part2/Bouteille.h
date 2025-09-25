/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Bouteille.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
// #include "utils.h"
using namespace std;

class Bouteille{
    
    
    
        
    
    public:
        Bouteille();
        virtual ~Bouteille();
        virtual void afficher()=0;

        
    
};

Bouteille::Bouteille(){}
Bouteille::~Bouteille(){}
void Bouteille::afficher(){
    
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille" << endl;
    cout << "----------------------------------------------------------------"<< endl;
}

