/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Soft.h v1
*/

#include <iostream>
#include <cmath>
using namespace std;


class Soft: public Bouteille{
    protected:
        double degres =8; // en %
    public:
        Soft();
        ~Soft();
        void afficher();
        
    
};

Soft::Soft(){}
Soft::~Soft(){}
void Soft::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille de Soft" << endl;
    cout << "----------------------------------------------------------------"<< endl;
}
