/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
using namespace std;


class Alcool: public Bouteille{
    protected:
        double degres; // en %
    public:
        Alcool();
        ~Alcool();
        void afficher();
        
    
};

Alcool::Alcool(){}
Alcool::~Alcool(){}
void Alcool::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille d'alcool" << endl;
    cout << "----------------------------------------------------------------"<< endl;
}
