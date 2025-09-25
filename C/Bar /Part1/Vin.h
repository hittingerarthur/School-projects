/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
#include <cstring>
using namespace std;


class Vin: public Alcool{
    
    protected: 

        int annee;
        string couleur;

    
    public:
        Vin();
        ~Vin();
        void afficher();
        string type(){return "Vin";}
        double prix(){
            if ((2023-annee)<=22){
                return 100;
            }
            else{
                return 100 + (5 * (2023-annee-22));
            }
            }
            

        
    
};

Vin::Vin(){
    
    
    cout << "---------------------------------------------------"<< endl;
    cout<<"Vous allez choisir votre bouteille de Vin   :"<<endl;
    cout << "---------------------------------------------------"<< endl;
    cout <<"\n";
    do{
        cout << "--------------------------------------"<< endl;
        cout <<"Choisissez le degres de la bouteille  :"<<endl;
        cout << "--------------------------------------"<< endl;
        cout << "choix : ";
        cin >> degres;
    }while(degres<8||degres>100);
    do{
        cout << "--------------------------------------"<< endl;
        cout <<"Choisissez l'annee de la bouteille  :"<<endl;
        cout << "--------------------------------------"<< endl;
        cout << "choix : ";
        cin >> annee;
    }while(annee<0||annee>2023);
    cout << "--------------------------------------"<< endl;
    cout <<"Choisissez la couleur de la bouteille  :"<<endl;
    cout << "--------------------------------------"<< endl;
    cout << "choix : ";
    cin >> couleur;
    // while(strlen(couleur) == 0);
    
    
}
Vin::~Vin(){}
void Vin::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille d'alcool" << endl;
    cout << "----------------------------------------------------------------"<< endl;
    cout << "- Degres    :   "<<degres<< " %" <<endl;
    cout << "- Type      :   "<<type()<<endl;
    cout << "- Annee     :   "<<annee<<endl;
    cout << "- Couleur   :   "<<couleur<<endl;
    cout << "- Prix      :   "<<prix()<<" euros"<<endl;    
}

