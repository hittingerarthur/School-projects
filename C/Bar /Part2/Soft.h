/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Soft.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;


class Soft: public Bouteille{
    protected:
        double degres =8; // en %
    public:
        Soft();
        virtual ~Soft();
        virtual void afficher()=0;
        virtual double prix()=0;
        virtual string type()=0;

        
    
};

Soft::Soft(){}
Soft::~Soft(){}
void Soft::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille de Soft" << endl;
    cout << "----------------------------------------------------------------"<< endl;
}
