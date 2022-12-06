#include <SFML/Graphics.hpp>
#include <SFML/Network.hpp>

#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>

#include "Graph.h"

using namespace std;
using namespace sf;

#define WIDTH 1400
#define HEIGHT 800

// Search button set up and interaction
void setSearchBar(RectangleShape &searchBar, RectangleShape &searchButton, CircleShape &searchGlass, VertexArray &searchGlassHandle)
{
    // Search Bar (text input)
    searchBar.setSize(Vector2f(700,32));
    searchBar.setPosition(Vector2f(((float) WIDTH)/4-5,16));
    searchBar.setOutlineThickness(3);
    searchBar.setOutlineColor(Color(69, 27, 82));
    searchBar.setFillColor(Color(45,45,45));

    // Search Button (purple rectangle at end)
    searchButton.setSize(Vector2f(50,32));
    searchButton.setOutlineThickness(3);
    searchButton.setOutlineColor(Color(69, 27, 82));
    searchButton.setPosition(Vector2f(((float) 3 * WIDTH)/4-5,16));
    searchButton.setFillColor(Color(69, 27, 82));

    // Search Glass
    searchGlass.setRadius(8);
    searchGlass.setFillColor(Color::Transparent);
    searchGlass.setOutlineColor(Color::White);
    searchGlass.setOutlineThickness(2.5);
    searchGlass.setPosition(Vector2f(((float) 3 * WIDTH)/4 + 10,20));

    // SearchGlass Handle
    searchGlassHandle[0].position = Vector2f(1076 , 30);
    searchGlassHandle[1].position = Vector2f(1075 , 34);
    searchGlassHandle[2].position = Vector2f(1085 , 38);
    searchGlassHandle[3].position = Vector2f(1083 , 41);
}
bool mouseOverSearchButtonHelper(RenderWindow &window, Mouse &mouse)
{
    return ((mouse.getPosition(window).x >= ((float) 3 * WIDTH)/4-5) &&
            (mouse.getPosition(window).x <= (((float) 3 * WIDTH)/4-5) + 50) &&
            mouse.getPosition(window).y >= 16 &&
            mouse.getPosition(window).y <= 48);
}
void mouseOverSearchButton(RenderWindow &window, Mouse &mouse, RectangleShape &searchButton, CircleShape &searchGlass, VertexArray &searchGlassHandle)
{
    if (mouseOverSearchButtonHelper(window, mouse))
    {
        searchButton.setFillColor(Color(69, 27, 82));
        searchButton.setOutlineColor(Color(69, 27, 82));
        searchGlass.setOutlineColor(Color(137, 136, 138));
        searchGlassHandle[0].color = Color(137, 136, 138);
        searchGlassHandle[1].color = Color(137, 136, 138);
        searchGlassHandle[2].color = Color(137, 136, 138);
        searchGlassHandle[3].color = Color(137, 136, 138);
    }
    else
    {
        searchButton.setFillColor(Color(116, 45, 138));
        searchButton.setOutlineColor(Color(116, 45, 138));
        searchGlass.setOutlineColor(Color(255, 255, 255));
        searchGlassHandle[0].color = Color(255, 255, 255);
        searchGlassHandle[1].color = Color(255, 255, 255);
        searchGlassHandle[2].color = Color(255, 255, 255);
        searchGlassHandle[3].color = Color(255, 255, 255);
    }
}

// Comparable algorithm set up
void setCompareAlgorithmsBox(RectangleShape &algorithmsCompare, Text &DFS, Text &BFS)
{
    // Box
    algorithmsCompare.setSize(Vector2f(200,100));
    algorithmsCompare.setPosition(Vector2f(WIDTH-algorithmsCompare.getSize().x, HEIGHT-algorithmsCompare.getSize().y));
    algorithmsCompare.setFillColor(Color(69, 27, 82));

    // Text
    DFS.setPosition(Vector2f(WIDTH-algorithmsCompare.getSize().x + 10, HEIGHT-algorithmsCompare.getSize().y + 10));
    BFS.setPosition(Vector2f(WIDTH-algorithmsCompare.getSize().x + 10, HEIGHT-algorithmsCompare.getSize().y + 50));
}

// Recommendation box
void setRecommendationBox(vector<RectangleShape*> &recommendations, Text &forYou)
{
    // Box
    float y_axis = 700;
    for (int i = 5 ; i >= 0 ; i--)
    {
        recommendations.emplace_back(new RectangleShape(Vector2f(400,100)));
        RectangleShape* r = recommendations.back();
        r->setPosition(Vector2f(WIDTH-r->getSize().x, (y_axis - r->getSize().y) - ((float) i * r->getSize().y)));
        r->setOutlineColor(Color(20,20,20));
        r->setOutlineThickness(4);
        r->setFillColor(Color(70,70,70));
    }

    // Text
    forYou.setFillColor(Color::White);
    forYou.setPosition(Vector2f(WIDTH - 250, 50));
}

// Filter Sidebar menu
void setFilterSidebarMenu(vector<RectangleShape*> &filters, Text &filterText, vector<Text*> &filterOptions)
{
    float y_axis = 200;
    for (int i = 0 ; i < 3 ; i++)
    {
        filters.emplace_back(new RectangleShape(Vector2f(200,100)));
        RectangleShape* f = filters.back();
        f->setPosition(Vector2f(0, y_axis + ((float) i * f->getSize().y)));
        f->setFillColor(Color(69, 27, 82));
        f->setOutlineColor(Color(20,20,20));
        f->setOutlineThickness(4);
    }

    filterText.setPosition(Vector2f(50, y_axis - 35));
    filterText.setFillColor(Color::White);

    filterOptions[0]->setString("Genre");
    filterOptions[1]->setString("Rating");
}

// Search function (beta)
void search(Event event, Mouse &mouse, RenderWindow &window, string &input)
{
    // 1. Set up clock
    // 2. Perform DFS and BFS then time them
    // 3.
    if ((event.type == Event::MouseButtonPressed && mouseOverSearchButtonHelper(window, mouse)) || (event.type == Event::KeyPressed && event.key.code == Keyboard::Return))
    {
        string searchInput = input;
        input.erase(input.begin(),input.end());
    }
}

void getImageFromURL(Http::Request &animeImage, Http::Response &imageResponse, Http &http, Texture &animeTexture)
{
    animeImage.setMethod(Http::Request::Get);
    animeImage.setUri("/images/anime/7/25761.jpg");
    animeImage.setHttpVersion(1,1);
    animeImage.setField("From","me");

    imageResponse = http.sendRequest(animeImage);

    string body = imageResponse.getBody();
    animeTexture.loadFromMemory(body.c_str(), imageResponse.getBody().size());
}

// Getting all the data
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

    RenderWindow window(VideoMode(WIDTH, HEIGHT), "Otakuverse");

    // Event
    Event event;

    // User input string
    string input;

    // Font
    Font font;
    font.loadFromFile("Amazon-Ember-Medium.ttf");

    // Otakuverse Logo
    Sprite logo;
    Texture logoTexture;
    logoTexture.loadFromFile("Otakuverse_logo.png");
    logo.setTexture(logoTexture);
    logo.setPosition(Vector2f(10,10));
    logo.setScale(Vector2f(.5,.5));

    // All elements of the search bar
    Text searchText("",font);
    searchText.setFillColor(Color(120,120,120));
    RectangleShape searchBar;
    RectangleShape searchButton;
    CircleShape searchGlass;
    VertexArray searchGlassHandle(sf::TriangleStrip, 4);
    setSearchBar(searchBar,searchButton, searchGlass, searchGlassHandle);

    // Comparable Algorithms Display
    RectangleShape algorithmsCompare;
    Text DFS("DFS: ", font);
    Text BFS("BFS: ", font);
    setCompareAlgorithmsBox(algorithmsCompare, DFS, BFS);

    // Recommended Anime Display
    vector<RectangleShape*> recommendations;
    Text forYou("For You...", font);
    setRecommendationBox(recommendations, forYou);

    // Filter Sidebar
    /*
    vector<RectangleShape*> filters;
    Text filterText("Filters", font);
    vector<Text*> filterOptions;
    setFilterSidebarMenu(filters, filterText);
    */

    // Mouse button
    Mouse mouse;

    // Clock
    Clock clock;

    // Loading the anime file
    map<int, Anime> mapper;
    loadCSV("anime_filtered_modified.csv", mapper);

    // Anime image
    Sprite animeImage;
    Texture animeTexture;
    Http http("127.0.0.0");
    Http::Request imageRequest;
    Http::Response imageResponse;
    getImageFromURL(imageRequest, imageResponse, http, animeTexture);

    while (window.isOpen())
    {
        while (window.pollEvent(event))
        {
            if (event.type == Event::Closed)
                window.close();

            else if (event.type == Event::TextEntered)
            {
                if (isprint(event.text.unicode) && searchText.getLocalBounds().width < 680)
                    input += event.text.unicode;
            }
            else if (event.type == Event::KeyPressed)
            {
                if (event.key.code == Keyboard::BackSpace)
                    if (!input.empty())
                        input.pop_back();
            }
            search(event, mouse, window, input);
        }

        // code for blinking cursor written by Mortal on https://en.sfml-dev.org/forums/index.php?topic=26927.0
        static Time text_effect_time;
        static bool show_cursor;

        text_effect_time += clock.restart();

        if (text_effect_time >= seconds(0.5f))
        {
            show_cursor = !show_cursor;
            text_effect_time = Time::Zero;
        }

        // Position of the text in the searchbar
        searchText.setPosition(((float) WIDTH)/4,10);

        // Displaying text in the search bar
        if (input.empty())
        {
            searchText.setString("Search Otakuverse...");
            searchText.setStyle(Text::Italic);
            searchText.setFillColor(Color(100,100,100));
        }
        else
        {
            searchText.setString(input + (show_cursor ? '_' : ' '));
            searchText.setStyle(Text::Regular);
        }

        mouseOverSearchButton(window,mouse,searchButton,searchGlass,searchGlassHandle);

        // Background
        window.clear(Color(20,20,20));

        // Search Bar
        window.draw(searchBar);
        window.draw(searchButton);
        window.draw(searchGlass);
        window.draw(searchGlassHandle);
        window.draw(searchText);

        // Comparable Algorithms Box
        window.draw(algorithmsCompare);
        window.draw(DFS);
        window.draw(BFS);

        // Recommendation box
        for (auto r : recommendations)
            window.draw(*r);
        window.draw(forYou);

        // Filter box
        /*
        for (auto r : filters)
            window.draw(*r);
        window.draw(filterText);
        */

        // Logo
        window.draw(logo);

        window.display();
    }
    return 0;
}