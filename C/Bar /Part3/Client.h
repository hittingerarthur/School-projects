/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * Alcool.h v1
*/

#include <iostream>
#include <cmath>
#include <string>
#include <vector>

using namespace std;

class Client{
protected :
    vector<Bouteille*> m_bouteille;
public :
    Client();
    void afficher();
    virtual void ajouter();
    void supprimer();
    virtual ~Client();
};

//---------constructeur/destructeur-------------

Client::Client(){}
Client::~Client(){m_bouteille.clear();}
void Client::ajouter(){
    int choix;
    do{
    cout<<"---------------------------"<<endl;
    cout<<"  Choisissez une bouteille   "<<endl;
    cout<<"---------------------------"<<endl;
    cout<<"1 - Alcool fort"<<endl;
    cout<<"2 - Vin"<<endl;
    cout<<"3 - Eau"<<endl;
    cout<<"4 - Soda"<<endl;
    cout<<"---------------------------"<<endl;
    cout<<" Choix : "<<endl;
    cin>>choix;
    }while(choix<1 || choix>4);

    switch (choix)
    {
    case 1:
        /* code */
        Alcool_fort a;
        
        m_bouteille.push_back(new a);
        break;
    case 2:
        /* code */
        Vin a;
        
        m_bouteille.push_back(new a);
        break;
    case 3:
        /* code */
        Eau a;
        
        m_bouteille.push_back(new a);
        break;
    case 4:
        /* code */
        Soda a;
        
        m_bouteille.push_back(new a);
        break;
    
    default:
        break;
    }

    

}

void Client::afficher(){
    for(int i = 0 ; i < m_bouteille.size(); i++)
    {
    cout<<"---------------------------------"<<endl;
    cout<<"     Bouteille numero " << i+1 <<endl;
    cout<<"---------------------------------"<<endl;
    m_bouteille[i]->afficher();
    cout<<"---------------------------------"<<endl;  
    }
}

void Client::supprimer(){
    int choix ;
    do{
        cout<< " quel vehicule voulez vous supprimer : " ;
        cin >> choix ;

    }while(choix<0 || choix>m_bouteille.size());
   
    m_bouteille.erase(m_bouteille.begin() + (choix-1));


}