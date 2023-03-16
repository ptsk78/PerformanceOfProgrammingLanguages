#include <chrono>
#include <iomanip>
#include <cstring>

using namespace std;
using namespace std::chrono;

// https://stackoverflow.com/questions/24686846/get-current-time-in-milliseconds-or-hhmmssmmm-format
std::string time_in_HH_MM_SS_MMM()
{
    auto now = system_clock::now();
    auto ms = duration_cast<milliseconds>(now.time_since_epoch()) % 1000;
    auto timer = system_clock::to_time_t(now);
    std::tm bt = *std::localtime(&timer);
    std::ostringstream oss;
    oss << std::put_time(&bt, "%Y-%m-%d %H:%M:%S"); // HH:MM:SS
    oss << '.' << std::setfill('0') << std::setw(3) << ms.count();

    return oss.str();
}

// this is to show if you are willing to customize your code, you can get great speed ups in C++

class CustomRandom {
    private:
        unsigned int x0;

    public:
        CustomRandom()
        {
            x0 = (duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count()) & 0xFFFFFFFF;
        }

        unsigned int rand()
        {
            // this magic comes from https://en.wikipedia.org/wiki/Linear_congruential_generator
            unsigned long long x = (x0 * 1664525 + 1013904223) & 0xFFFFFFFF;
            x0 = x;
            return x0;
        }
};

class CustomString {
    private:
        unsigned int length;
        unsigned int maxLength;
        char *characters;
    public:
        CustomString()
        {
            maxLength = 1000;
            length = 0;
            characters = new char[maxLength];
            memset(characters, 0, maxLength);
        }
        
        CustomString(CustomString &idx)
        {
            length = idx.length;
            maxLength = length + 1;
            characters = new char[maxLength];
            characters[length] = 0;
            memcpy(characters, idx.characters, idx.length);
        }

        ~CustomString()
        {
            delete[] characters;
        }

        CustomString& operator+=(char s)
        {
            if (length >= maxLength - 2)
            {
                maxLength += 1000;
                char *charactersNew;
                charactersNew = new char[maxLength];
                memset(charactersNew + length + 1, 0, maxLength - length - 1);
                memcpy(charactersNew, characters, length);
                delete[] characters;
                characters = charactersNew;
            }
            characters[length] = s;
            length++;

            return *this;
        }

        bool operator==(CustomString &right)
        {
            if(length!=right.length)
            {
                return false;
            }
            for(int i=0;i<length;i++)
            {
                if(characters[i]!=right.characters[i])
                {
                    return false;
                }
            }
            return true;
        }

        char* c_str()
        {
            return characters;
        }
        
        unsigned int size()
        {
            return length;
        }
};

template <class T>
class CustomMember {
    public:
        CustomString* input;
        T* output;
        
        // this could be obviously improved if wanted
        CustomMember* next;

        CustomMember()
        {
            input = NULL;
            next = NULL;
            output = NULL;
        }
        
        ~CustomMember()
        {
            if(next!=NULL)
            {
                delete next;
            }
            
            if(input!=NULL)
            {
                delete input;
            }
            if(output!=NULL)
            {
                delete output;
            }
        }
        
        T& get(CustomString &idx)
        {
            if(output == NULL)
            {
                input = new CustomString(idx);
                output = new T[1];
                return output[0];
            }
            
            if((*input) == idx)
            {
                return output[0];
            }
            
            if(next==NULL)
            {
                next = new CustomMember();
                return next->get(idx);
            }
            
            return next->get(idx);
        }
        
        unsigned int size()
        {
            if(output==NULL)
            {
                return 0;
            }
            if(next==NULL)
            {
                return 1;
            }
            return 1 + next->size();
        }
};

#define HOWFAR 25

// this is obviously only string to T, not generic
// it should be not that hard to make it more generic
template <class T>
class CustomDictionary {
    private:
        CustomMember<T> *map;
        
        // there still might be a better hash map function...
        unsigned int getindex(CustomString &idx)
        {
            char *p = idx.c_str();
            unsigned int l = idx.size();
            unsigned long long x = 0; 
            
            for(int i=0;i<int((l-1)/4)+1;i++)
            {
                unsigned int tmp = 0;
                int hm = 4;
                if(int((l-1)/4) == i)
                {
                    hm = l - 4 * i;
                }
                if(hm==4)
                {
                    memcpy(&tmp, &(p[i*4]), 4);
                }
                else
                {
                    memcpy(((char*)&tmp)+(4-hm), &(p[i*4]), hm);
                }
                x = (x * 1664525 + 1013904223 + tmp) & 0xFFFFFFFF;
            }
            x = x % (1<<HOWFAR);
            return x;
        }
    public:
        CustomDictionary()
        {
            map = new CustomMember<T>[1<<HOWFAR];
        }
        
        ~CustomDictionary()
        {
            delete[] map;
        }
        
        T& operator[](CustomString &idx)
        {
            unsigned int id = getindex(idx);
            
            return map[id].get(idx);
        }
        
        size_t size()
        {
            size_t ret = 0;
            
            for(int i=0;i<(1<<HOWFAR);i++)
            {
                ret += map[i].size();
            }
            
            return ret;
        }
};

// this is same as C++, but using custom classes instead
int main ()
{
    CustomRandom cr;
    CustomDictionary<bool> cd;
    char letter[] = "qwertyuiopasdfghjklz\0";

    for(int i=0;i<5000001;i++)
    {
        if(i%1000000==0)
        {
            printf("%s\n", time_in_HH_MM_SS_MMM().c_str());
        }

        CustomString s;
        for(int j=0;j<50;j++)
        {
            s += letter[cr.rand()%20];
        }
        cd[s] = true;
    }

    return 0;
}
