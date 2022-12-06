#include <iostream>
#include <vector>
#include <string>
using namespace std;


class Anime {
public:
    int animeID;
    string title;
    string imageURL;
    string genre;

    Anime(int id = 0, string name = "", string url = "", string category = ""){
        animeID = id;
        title = name;
        imageURL = url;
        genre = category;
    }

    void Print() {
        cout << "Anime ID: " << animeID << endl;
        cout << "Anime Title: " << title << endl;
        cout << "Anime URL: " << imageURL << endl;
        cout << "Anime Genre: " << genre << endl;
        cout << endl;
    }
};

class Graph {
private:
    vector<vector<int>> graph;

public: 
    Graph(){}

    void insert(Anime newVertex, int index) {
        graph[index][index] = 0;
    }

    vector<vector<int>> GetGraph() {
        return graph;
    }
};
