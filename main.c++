#include <iostream>
#include <iterator>
#include <map>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <string>

using namespace std;

// https://stackoverflow.com/questions/24686846/get-current-time-in-milliseconds-or-hhmmssmmm-format
std::string time_in_HH_MM_SS_MMM()
{
    using namespace std::chrono;
    auto now = system_clock::now();
    auto ms = duration_cast<milliseconds>(now.time_since_epoch()) % 1000;
    auto timer = system_clock::to_time_t(now);
    std::tm bt = *std::localtime(&timer);
    std::ostringstream oss;
    oss << std::put_time(&bt, "%Y-%m-%d %H:%M:%S"); // HH:MM:SS
    oss << '.' << std::setfill('0') << std::setw(3) << ms.count();

    return oss.str();
}

int main ()
{
    map<string, bool> dic;
    char letter[] = "qwertyuiopasdfghjklz\0";

    for(int i=0;i<5000001;i++)
    {
        if(i%1000000==0)
        {
            printf("%s\n", time_in_HH_MM_SS_MMM().c_str());
        }

        string s = "";
        for(int j=0;j<50;j++)
        {
            s += letter[rand()%20];
        }
        dic[s] = true;
    }
    return 0;
}
