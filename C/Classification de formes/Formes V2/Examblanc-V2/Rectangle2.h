//
//  Rectangle2.h
//  Examblanc-V2
//
//  Created by Arthur Hittinger on 28/03/2024.
//

#include<iostream>
#include<cmath>

using namespace std;

//----------------------------------
class rectangle: public carre{
//----------------------------------
protected:
    double largeur;
public:
    //methodes
           rectangle(double=0,double=0);
    virtual void   afficher();
    virtual double perimetre();
    virtual double aire();
    virtual int    type();

};
//------------------------------------------------
rectangle::rectangle(double a,double b):carre(a),largeur(b){}

double rectangle::perimetre()
{
    return(2*(x+largeur));
}

double rectangle::aire()
{
    return(x*largeur);
}

int rectangle::type(){return(3);}

void rectangle::afficher()
{
    cout<<"----------------------"<<endl;
    cout<<"c'est un rectangle"<<endl;
    cout<<"----------------------"<<endl;
    cout<<"longeur   :  "<<x<<endl;
    cout<<"largeur   :  "<<largeur<<endl;
    cout<<"perimetre :  "<<rectangle::perimetre()<<endl;
    cout<<"aire      :  "<<rectangle::aire()<<endl;
    cout<<"type      :  "<<rectangle::type()<<endl;
    cout<<"----------------------"<<endl;
}

