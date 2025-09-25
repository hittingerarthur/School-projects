//
//  main.cpp
//  ExamBlanc-V3
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include<iostream>
#include<math.h>
#include<vector>
#include "Forme3.h"
#include "Cercle3.h"
#include "Carre3.h"
#include "Rectangle3.h"
#include "MesFormes.h"
using namespace std;

int main(int argc, const char * argv[]) {

    
    
    Mes_formes g;
    int choix;
    do{
     system("cls");

     choix = Menu("Forme");
     if (choix == 1){
         g.ajouter();
         system("pause");
     }
     if (choix == 2){
         g.afficher();
         system("pause");
     }
     if (choix == 3){
         g.supprimer();
         system("pause");
     }
    }while(choix!=4);
    cout << "Gracias, Ciao" << endl;
 
    return 0;
}
