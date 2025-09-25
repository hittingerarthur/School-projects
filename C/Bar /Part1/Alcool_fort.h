/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;


class Alcool_fort: public Alcool{
    protected:
        int indice;
    
    public:
        Alcool_fort();
        ~Alcool_fort();
        void afficher();
        string type(){return "Alcool Fort";}
        double prix(){return 50;}

        
    
};

Alcool_fort::Alcool_fort(){
    
    
    cout << "---------------------------------------------------"<< endl;
    cout<<"Vous allez choisir votre bouteille d'Alcool Fort   :"<<endl;
    cout << "---------------------------------------------------"<< endl;
    cout <<"\n";
    do{
        cout << "--------------------------------------"<< endl;
        cout <<"Choisissez la bouteille d'alcool fort  :"<<endl;
        cout << "--------------------------------------"<< endl;
        cout << "1 - Vodka"<< endl;
        cout << "2 - Rhum"<< endl;
        cout << "3 - Whisky"<< endl;
        cout << "4 - Gin"<< endl;
        cout << "5 - Tequila"<< endl;
        cout << "6 - Pastis"<< endl;
        cout << "--------------------------------------"<< endl;
        cout << "choix : ";
        cin >> indice;

    }while(indice<1 || indice>6);

    switch (indice)
        {
        case 1:
            /* code */
            degres = 37.5;
            break;
        case 2:
            /* code */
            degres = 37.5;
            break;
        case 3:
            /* code */
            degres = 40;
            break;
        case 4:
            /* code */
            degres = 37.5;
            break;
        case 5:
            /* code */
            degres = 55;
            break;
        case 6:
            /* code */
            degres = 45;
            break;
        
        default:
            break;
        }
}
Alcool_fort::~Alcool_fort(){}
void Alcool_fort::afficher(){
    cout << "----------------------------------------------------------------"<< endl;
    cout << "C'est une bouteille d'alcool" << endl;
    cout << "----------------------------------------------------------------"<< endl;
    cout << "- Degres    :   "<<degres<< " %" <<endl;
    
    cout << "- Type      :   "<<type()<<endl;
    /**
     * cout << "1 - Vodka"<< endl;
        cout << "2 - Rhum"<< endl;
        cout << "3 - Whisky"<< endl;
        cout << "4 - Gin"<< endl;
        cout << "5 - Tequila"<< endl;
        cout << "6 - Pastis"<< endl;
    */
    switch (indice)
        {
        case 1:
            /* code */
            cout << "- genre:    :   "<<"Vodka"<<endl;
            break;
        case 2:
            /* code */
            cout << "- genre:    :   "<<"Rhum"<<endl;
            break;
        case 3:
            /* code */
            cout << "- genre:    :   "<<"Whisky"<<endl;
            break;
        case 4:
            /* code */
            cout << "- genre:    :   "<<"Gin"<<endl;
            break;
        case 5:
            /* code */
            cout << "- genre:    :   "<<"Tequila"<<endl;
            break;
        case 6:
            /* code */
            cout << "- genre:    :   "<<"Pastis"<<endl;
            break;
        
        default:
            break;
        }
        cout << "- Prix      :   "<<prix()<< " euros"<<endl;

    
}

