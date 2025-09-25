/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;


class Alcool: public Bouteille{
    protected:
        double degres; // en %
    public:
        Alcool();
        virtual ~Alcool();
        virtual void afficher()=0;
        virtual double prix()=0;
        virtual string type()=0;
        
    
};

Alcool::Alcool(){}
Alcool::~Alcool(){}
void Alcool::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille d'alcool" << endl;
    cout << "----------------------------------------------------------------"<< endl;
}
