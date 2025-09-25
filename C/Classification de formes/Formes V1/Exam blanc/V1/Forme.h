//
//  Forme.h
//  Exam blanc/Users/arthurhittinger/Desktop/In323/Exam blanc/Exam blanc/V1/Forme.h
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#define Forme_h
#include <iostream>
using namespace std;



class forme{
//----------------------------------
protected:
    //attributs
       double x;

public:
    //methodes
    forme(double=0);
    void afficher();

};

//----------------------------------
// Definition des methodes
//----------------------------------
forme:: forme(double a):x(a){} // constructeur

void forme::afficher()
{
    cout<<"C'est une forme "<< endl;
}



