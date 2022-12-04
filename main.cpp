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