//
//  Forme3.h
//  ExamBlanc-V3
//
//  Created by Arthur Hittinger on 28/03/2024.
//

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
    virtual void afficher()=0;
    virtual double perimetre()=0;
    virtual double aire()=0;
    virtual int    type()=0;
    
    virtual ~forme(){};


};

//----------------------------------
// Definition des methodes
//----------------------------------
forme:: forme(double a):x(a){} // constructeur

void forme::afficher()
{
    cout<<"C'est une forme "<< endl;
}



