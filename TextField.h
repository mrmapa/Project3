#include <SFML/Graphics.hpp>


class TextField : public sf::Transformable, public sf::Drawable {

private:
    unsigned int m_size;
    sf::Font m_font;
    std::string m_text;
    sf::RectangleShape m_rect;
    bool m_hasfocus;

public:
    TextField(unsigned int maxChars);
    const std::string getText() const;
    void setPosition(float x, float y);
    bool contains(sf::Vector2f point) const;
    void setFocus(bool focus);
    void handleInput(sf::Event e);
};