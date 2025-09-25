//
//  Mes_formes.h
//  ExamBlanc-V3
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include<iostream>
#include<math.h>
#include<vector>
using namespace std;

class Mes_formes{
protected:
    vector<forme *> L;
public:
    Mes_formes(){};
    virtual ~Mes_formes(){};
    void ajouter();
    void supprimer();
    virtual void afficher();

};

// -------------------------------------------------
 void informations ( forme *v ) {
      v -> afficher();
 }

 int  Menu(string s){
     int choix;
     do{
        cout << "\n\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\t       Menu "<< s <<"\n";
        cout << "\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\t1 - Ajouter   "<< s <<"\n";
        cout << "\t\t\t\t\t2 - Afficher  "<< s <<"\n";
        cout << "\t\t\t\t\t3 - Supprimer "<< s <<"\n";
        cout << "\t\t\t\t\t4 - Quitter\n";
        cout << "\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\tChoix : ";
        cin >> choix;
     }while(choix < 1 || choix > 4);
     return choix;
 }

 int  Menu_ajouter(){
     int choix;
     do{
        cout << "\n\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\t       Ajouter\n";
        cout << "\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\t1 - Cercle \n";
        cout << "\t\t\t\t\t2 - Carre  \n";
        cout << "\t\t\t\t\t3 - Rectangle  \n";
        cout << "\t\t\t\t\t-------------------------\n";
        cout << "\t\t\t\t\tChoix : ";
        cin >> choix;
     }while(choix < 1 || choix > 3);
     return choix;
 }

 void Mes_formes :: ajouter(){
    int choix = Menu_ajouter();
    if (choix == 1 ){
        cout << "\t\t\t\t\t -------- Cercle --------" << endl;
        cout << "\t\t\t\t\t Rayon : ";
        int p;
        cin >> p;
        L.push_back(new cercle(p));
    }
    if (choix == 2 ){
        cout << "\t\t\t\t\t -------- Carre --------" << endl;
        cout << "\t\t\t\t\t Cote : ";
        int p;
        cin >> p;
        L.push_back(new carre(p));
    }
    if (choix == 3 ){
        cout << "\t\t\t\t\t -------- Rectangle --------" << endl;
        cout << "\t\t\t\t\t Longueur : ";
        int p;
        cin >> p;
        cout << "\t\t\t\t\t Largeur : ";
        int l;
        cin >> l;
        L.push_back(new rectangle(p,l));
    }
 }

 void Mes_formes :: afficher(){

     cout << "\t\t\t\t\t----- vous avez " << L.size() << " formes -----" << endl ;
     for ( int i =0 ; i< L.size(); i++)
     {
         L[i]->afficher();
     }
 }

  void Mes_formes :: supprimer(){int n ;
      do{
      cout << "\n\t\t\t\t\tDonnez le numero de forme a supprimer : " ;
      cin >>  n ;
      }while( n<0 || n> L.size());
      L.erase(L.begin()+n);

     cout << "\n\t\t\t\t\tLa forme a ete supprime avec sucess !!\n " ;
  }

