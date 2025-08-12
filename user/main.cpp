#include<iostream>
#include <thread>
#include <chrono>
#include <string>


using namespace std;

    const string BLUE   = "\033[34m";      // colors
    const string YELLOW = "\033[33m";
    const string RED    = "\033[31m";      
    const string GREEN  = "\033[32m";
    const string RESET  = "\033[0m";     // defult color

int app_choise;


void loading(){

        cout << RED;
        cout << " "<<endl;
        cout << " "<<endl;
        cout << "                  __              ___                          " <<endl;
        cout << "                  / / ___ ___ ____/ (____ ___ _                " <<endl;
        cout << "                  / /_/ _ / _ `/ _  / / _ / _ `/ _ _ _ _       " <<endl;
        cout << "                  /____\\__\\_,_/\\_,_/_/_//_\\_, / (_(_(_(_)     " <<endl;
        cout << "                                          /___/                " <<endl;
        cout << "                                                               " <<endl;

       cout << " "<<endl;
       cout<< BLUE;
       cout << "          please wait for " << 5  << " seconds... " <<endl;
       this_thread::sleep_for(chrono::seconds(5));
       system("clear");
       cout << RESET;
}


void choise_english(){
    cout << "  "<<endl;
    cout << "  "<<endl;
    cout << " Please review the details below and select your choise "<<endl;
    cout << "   1.for audio communication enter 1 "<<endl;
    cout << "   2.for video communication enter 2 "<<endl;
    cout << "   3.for help enter 3"<<endl;
    cout << "   4.for our service details enter 4"<<endl;
    cout << "   5. contact buliders "<<endl;
    cout << " "<<endl;
    cout << " Enter your choise here: ";
    cin>>app_choise;
}

void choise_amharic(){
    cout << "  "<<endl;
    cout << "  "<<endl;
    cout << "       እባክዎ ከታች ያሉትን ዝርዝሮች ተመልክተ ው ይምረጡ👇👇👇👇   "<<endl;
    cout << "          "<<endl;
    cout << " 1.ለድ ምጽ ግንኙነት አንድን(1) ይጫኑ                           "   <<endl;
    cout << " 2.ለምስል ግንኙነት ሁ ለትን(2) ይ ጫኑ                          "   <<endl;
    cout << " 3.ለእርዳታ ሶስትን(3) ይ ጫኑ                                   "   <<endl;
    cout << " 4.ስለ አገልግሎቶቻችን ለማወ ቅ አራትን(4) ይጫኑ.                  "   <<endl;
    cout << " 5.ባለሙ ያዎ ችን ለ ማግኘት አ ምስትን(5) ይጫኑ.                  "   <<endl;
    cout << " "<<endl;
    cout << "  የእርስዎን ምላሽ ምላሽ ያስገቡ: ";
    cin>>app_choise;
}

void choise_oromic(){
    cout << " " <<endl;
    cout << " " <<endl;
    cout << "         Mee Bal'ina isaa armaan gadii ilaalaa " <<endl;
    cout << " " <<endl;
    cout << " 1. weliqunemti segelef tokko tuqa " <<endl;
    cout << " 2. weliqunemti fekif lakofisa lama tuqa " <<endl;
    cout << " 3.degerisav lakofisa 3 tuqa " <<endl;
    cout << " 4.wae tejajila kenys bekuf lakofisa 4 tuqa" <<endl;
    cout << " 5. mamiltota arigechuf lakofisa 5 tuqa " <<endl;
    cout << " " <<endl;
    cout << " Deebii keessan galchaa: " ;
    cin>>app_choise;
}

void language(){

    int choise;
    cout << " "<<endl;

          cout << " 1. For English please enter 1              "<<endl;
          cout << " 2. ለአማርኛ እባክዎ 2 ን ያስገቡ                  "<<endl;
          cout << " 3. Afan oromof lakofisa 3 tuqa             "<<endl;
          cout << " 4.                                         "<<endl;
          cout << " 5.                                         "<<endl;
          cout << " "<<endl;
          cout << " Enter your choise here: ";
          cin>>choise;
       if(choise == 1){
        choise_english();
       }
       else if(choise == 2){
        choise_amharic();
       }
       else if(choise == 3){
        choise_oromic();
       }
       else if(choise == 4){
        cout << " coming soon ";
        cout << " "<<endl;
       }
       else if(choise == 5){
        cout << " coming soon ";
        cout << " "<<endl;
       }
       else{
        cout << "No language found with choise please enter valid number of choise"<<endl;
        cout << " "<<endl;
       }
}


void app_choise_fun(){
    if(app_choise == 1){
        system("clear");
        system("python3 audio_script/audio.py");
    }
    else if( app_choise == 3){
        system("cat ../help/help.txt");
    }
    else {
        cout << "Invalid choise"<<endl;
    }
}

int main(){

    loading();
    language();
    app_choise_fun();
    
    return 0;
}
