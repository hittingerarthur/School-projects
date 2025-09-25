/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;


class Eau: public Soft{
    
    protected:
        int indice;
    
    public:
        Eau();
        ~Eau();
        void afficher();
        string type(){return "Eau";}
        double prix();
        
    
};

Eau::Eau(){
    
    
    
    do{
        cout <<"Choisissez la bouteille d'eau  :"<<endl;
        cout << "--------------------------------------"<< endl;
        cout << "1 - Plate"<< endl;
        cout << "2 - Gazeuse"<< endl;
        cout << "--------------------------------------"<< endl;
        cout << "choix : ";
        cin >> indice;

    }while(indice<1 || indice>2);

    switch (indice)
        {
        case 1:
            /* code */
            indice = 1;
            break;
        case 2:
            /* code */
            indice = 2;
            break;
        
        
        default:
            break;
        }
}
Eau::~Eau(){}

double Eau::prix(){
    
    switch (indice)
    {
    case 1:
        /* code */
        return 3;
        break;
    case 2:
        /* code */
        return 5;
        break;
    
    default:
        break;
    }
            
            
}
void Eau::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille de soft" << endl;
    cout << "----------------------------------------------------------------"<< endl;
    cout << "- Type            :   "<<type() <<endl;
    
    switch (indice)
    {
    case 1:
        cout << "- Petillante      :   non"<<endl;
        break;
    case 2:
        cout << "- Petillante      :   oui"<<endl;
        
        break;
    
    default:
        break;
    }
    cout << "- Prix            :   "<<prix()<< " euros"<<endl;

    
}

