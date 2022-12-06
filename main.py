import pygame, sys
from constants import *

def setSearchBar(searchText, input, font, screen):
    # search bar
    searchBar_back = pygame.Surface((706, 38))
    searchBar_back.fill(PURPLE)
    searchBar_back_rect = searchBar_back.get_rect(topleft = (WIDTH/4 - 8, 13))
    screen.blit(searchBar_back, searchBar_back_rect)

    searchBar = pygame.Surface((700, 32))
    searchBar.fill([45, 45, 45])
    searchBar_rect = searchBar.get_rect(topleft = (WIDTH/4 - 5, 16))
    screen.blit(searchBar, searchBar_rect)

    # search button
    searchButton_back = pygame.Surface((56, 38))
    searchButton = pygame.Surface((50, 32))
    searchButton_back_rect = searchButton_back.get_rect(topleft = ((3 * WIDTH)/4 - 8, 13))
    searchButton_rect = searchButton.get_rect(topleft = ((3 * WIDTH)/4 - 5, 16))
    searchButton.fill(LIGHT_PURPLE)
    searchButton_back.fill(LIGHT_PURPLE)
    screen.blit(searchButton_back, searchButton_back_rect)
    screen.blit(searchButton, searchButton_rect)

    # search glass

    # search glass handle

    # search text
    if input == "":
        searchText = font.render("Search...", False, (120, 120, 120))
    else:
        searchText = font.render(input, False, (120, 120, 120))

    screen.blit(searchText, searchBar_rect)
def setRecommendationBox(forYou, screen):
    new_rec = pygame.Surface((400, 600))
    new_rec.fill([70, 70, 70])
    new_rec_rect = new_rec.get_rect(topleft = (WIDTH - 400, 100))
    screen.blit(new_rec, new_rec_rect)

    for i in range(0, 4):
        pygame.draw.line(screen, [20, 20, 20], (WIDTH - 400, 100 + 120 * (i + 1)), (WIDTH, 100 + 120 * (i + 1)), 4)
    
    forYou_rect = forYou.get_rect(topleft = (WIDTH - 250, 50))
    screen.blit(forYou, forYou_rect)

def setCompareAlgorithmsBox(dfs, bfs, screen):
    algorithms = pygame.Surface((200, 100))
    algorithms.fill(PURPLE)
    algorithms_rect = algorithms.get_rect(topleft = (WIDTH-200, HEIGHT-100))
    screen.blit(algorithms, algorithms_rect)

    dfs_rect = dfs.get_rect(topleft = (WIDTH - 200 + 10, HEIGHT - 100  + 10))
    bfs_rect = bfs.get_rect(topleft = (WIDTH - 200 + 10, HEIGHT - 100 + 50))
    screen.blit(dfs, dfs_rect)
    screen.blit(bfs, bfs_rect)

def userRatingBarSetup(smallFont, bigFont, screen):
    # bar
    for i in range(0, 10):
        userRatingText = bigFont.render("  " + str(i+1), False, (255, 255, 255))
        userRating = pygame.Surface((100, 100))
        userRating_rect = userRating.get_rect(topleft = (100 * i, HEIGHT-100))
        userRating.fill(PURPLE)
        screen.blit(userRating, userRating_rect)
        screen.blit(userRatingText, userRating_rect)
        pygame.draw.line(screen, [20, 20, 20], (100 * (i+1), HEIGHT-100), (100 * (i+1), HEIGHT), 6)

    # text above bar
    ratingText = smallFont.render("Give us your rating for anime above: ", False, (255,255,255))
    ratingTitle = pygame.Surface((200, 100))
    ratingTitle_rect = ratingTitle.get_rect(topleft = (230, HEIGHT - 150))
    screen.blit(ratingText, ratingTitle_rect)

def inputRating(input_rating, font, screen):
    inputString = str(input_rating)
    inputRatingText = font.render("Your Rating: " + inputString, False, (255, 255, 255))
    inputRatingSurface = pygame.Surface((200, 100))
    inputRating_rect = inputRatingSurface.get_rect(topleft = (1000, HEIGHT-100))
    screen.blit(inputRatingText, inputRating_rect)

def main():
    # initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Otakuverse")

    input = ""

    screen.fill([20, 20, 20])

    # loading font
    font = pygame.font.Font("Amazon-Ember-Medium.ttf", 30)
    userRatingFont = pygame.font.Font("Amazon-Ember-Medium.ttf", 50)
    inputRatingFont = pygame.font.Font("Amazon-Ember-Medium.ttf", 25)

    # loading logo
    logo = pygame.image.load("Otakuverse_logo.png")
    logo = pygame.transform.scale(logo, LOGO_SIZE)

    logo_rect = logo.get_rect(topleft = (10, 10))
    screen.blit(logo, logo_rect)

    # loading search bar
    searchText = font.render("Search...", False, (120, 120, 120))
    setSearchBar(searchText, input, font, screen)

    # comparable algorithms display
    dfs = font.render("DFS: ", False, [255, 255, 255])
    bfs = font.render("BFS: ", False, [255, 255, 255])
    setCompareAlgorithmsBox(dfs, bfs, screen)
    
    # recommended anime display
    forYou = font.render("For You...", False, [255, 255, 255])
    setRecommendationBox(forYou, screen)

    # loading user rating bar
    input_rating = 0
    userRatingBarSetup(font, userRatingFont, screen)
    inputRating(input_rating, inputRatingFont, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                else:
                    input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (0 <= pygame.mouse.get_pos()[0] <= 1000 and
                    HEIGHT-100 <= pygame.mouse.get_pos()[1] <= HEIGHT):
                        input_rating = (pygame.mouse.get_pos()[0] // 100) + 1

            screen.fill((20, 20, 20))

            setSearchBar(searchText, input, font, screen)
            setRecommendationBox(forYou, screen)
            setCompareAlgorithmsBox(dfs, bfs, screen)
            userRatingBarSetup(font, userRatingFont, screen)
            inputRating(input_rating, inputRatingFont, screen)
            screen.blit(logo, logo_rect)

            pygame.display.update()

if __name__ == "__main__":
    main()
