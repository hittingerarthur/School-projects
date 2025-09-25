/**
 * Partiel In323 - c++
 * Victor Guermonprez 3PSC1
 * version1.cpp v1
*/

#include <iostream>
#include <cmath>
#include <string>
#include <fstream>
#include "Bouteille.h"
#include "Alcool.h"
#include "Soft.h"
#include "Vin.h"
#include "Eau.h"

#include "Soda.h"
#include "Alcool_fort.h"
#include "Client.h"
using namespace std;

/**
 * Programme principal
*/
main(){
    Client c;
    int choix;
    do{
        do{
            system("cls");
            cout<<"----------------------------------------------------------------"<<endl;
            cout << "Menu Bouteilles   "<<endl;
            cout<<"----------------------------------------------------------------"<<endl;
            cout<<"1- Ajouter "<<endl;
            cout<<"2- Supprimer "<<endl;
            cout<<"3- Afficher "<<endl;
            cout<<"4- Sortir "<<endl;

            

        }while(choix<1||choix>4);
        switch(choix){
            case 1:
                c.ajouter();
                break;
            case 2:
                c.supprimer();
                break;
            case 3:
                c.afficher();
                break;
            
    }


    }while(choix != 4);
    
}