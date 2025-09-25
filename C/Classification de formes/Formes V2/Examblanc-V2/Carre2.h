//
//  Carre2.h
//  Examblanc-V2
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include<iostream>
#include<cmath>

using namespace std;

//----------------------------------
class carre: public forme{
//----------------------------------
public:
    //methodes
           carre(double=0);
    virtual void afficher();
    virtual double perimetre();
    virtual double aire();
    virtual int    type();
    
    virtual ~carre(){};



};
//------------------------------------------------
carre::carre(double a):forme(a){}

double carre::perimetre()
{
    return(x*4);
}

double carre::aire()
{
    return(pow(x,2));
}

int carre::type(){return(2);}

void carre::afficher()
{
    cout<<"----------------------"<<endl;
    cout<<"c'est un carre"<<endl;
    cout<<"----------------------"<<endl;
    cout<<"rayon     :  "<<x<<endl;
    cout<<"perimetre :  "<<carre::perimetre()<<endl;
    cout<<"aire      :  "<<carre::aire()<<endl;
    cout<<"type      :  "<<carre::type()<<endl;
    cout<<"----------------------"<<endl;
}
