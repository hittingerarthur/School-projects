/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;


class Soda: public Soft{
    
    protected:
        int indice;
    
    public:
        Soda();
        virtual ~Soda();
        virtual void afficher();
        virtual string type(){return "Soda";}
        virtual double prix();
        
    
};

Soda::Soda(){
    
    
    
    do{
        cout << "--------------------------------------"<< endl;
        cout <<"Choisissez la bouteille de soda  :"<<endl;
        cout << "--------------------------------------"<< endl;
        cout << "1 - normale"<< endl;
        cout << "2 - light"<< endl;
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
Soda::~Soda(){}

double Soda::prix(){
   return 4;   
}
void Soda::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille de soft" << endl;
    cout << "----------------------------------------------------------------"<< endl;
    cout << "- Type            :   "<<type() <<endl;
    
    
    switch (indice)
    {
    case 1:
        cout << "- Light           :   non"<<endl;
        
        break;
    case 2:
        cout << "- Light           :   oui"<<endl;
        
        
        break;
    
    default:
        break;

    }
    cout << "- Prix            :   "<<prix()<< " euros"<<endl;
    cout << "----------------------------------------------------------------"<< endl;
    

    
}

