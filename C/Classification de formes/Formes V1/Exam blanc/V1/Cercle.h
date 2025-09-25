//
//  Cercle.h
//  Exam blanc
//
//  Created by Arthur Hittinger on 28/03/2024.
//


#include<iostream>
#include<cmath>

using namespace std;

//----------------------------------
class cercle: public forme{
//----------------------------------
public:
    //methodes
           cercle(double=0);
    void   afficher();
    double perimetre();
    double aire();
    int    type();

};
//------------------------------------------------
cercle::cercle(double a):forme(a){}

double cercle::perimetre()
{
    return(M_PI*x*2);
}

double cercle::aire()
{
    return(M_PI*pow(x,2));
}

int cercle::type(){return(1);}

void cercle::afficher()
{
    cout<<"----------------------"<<endl;
    cout<<"c'est un cercle"<<endl;
    cout<<"----------------------"<<endl;
    cout<<"rayon     :  "<<x<<endl;
    cout<<"perimetre :  "<<cercle::perimetre()<<endl;
    cout<<"aire      :  "<<cercle::aire()<<endl;
    cout<<"type      :  "<<cercle::type()<<endl;
    cout<<"----------------------"<<endl;
}
