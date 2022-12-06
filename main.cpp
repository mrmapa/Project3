/*
#include <SFML/Graphics.hpp>
#include "TextField.h"
#include <iostream>
#include <map>

using namespace std;
using namespace sf;

#define width 1400
#define height 800

int main() {
    RenderWindow window(VideoMode(width, height), "Otakuverse");

    TextField searchbar(20);
    while (window.isOpen())
    {
        Event event;
        string input;
        Text search;
        Font font;

        while (window.pollEvent(event))
        {
            if (event.type == Event::Closed)
                window.close();



        }
        window.clear();
        window.draw(search);
        window.display();
    }
    return 0;
}
// Mapa was here
*/

#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <map>
#include "Graph.h"
using namespace std;

void loadCSV(const string& filename, map<int, Anime>& mapper) {
    ifstream inFile(filename);

    //reads the first line of data
    string lineFromFile;
    getline(inFile, lineFromFile);

    int index = 0;

    while(getline(inFile, lineFromFile) && index < 1000){
        //stream of data from a string
        istringstream stream(lineFromFile);

        int animeID;
        string title;
        string imageURL;
        const string urlFix = "https://cdn.myanimelist.net";
        string genre;
        string temp;

        getline(stream, temp, ';');
        animeID = stoi(temp);
        string name;
        getline(stream, name, ';');
        getline(stream, temp, ';');
        getline(stream, temp, ';');
        getline(stream, temp, ';');
        getline(stream, imageURL, ';');

        for(int i = 0; i < 22; i++) {
            getline(stream, temp, ';');
        }

        getline(stream, genre, ';');

        imageURL.replace(0, 32, urlFix);

        //creates an object from the information
        Anime anime(animeID, name, imageURL, genre);
        mapper[index] = anime;
        //mapper[index].Print();
        index++;
    }
}

int main() {
    map<int, Anime> mapper;

    loadCSV("C:/Users/derek/Documents/GitHub/Project3/src/anime_filtered_modified.csv", mapper);

    for(auto iter: mapper) {
        iter.second.Print();
    }


    return 0;
}
