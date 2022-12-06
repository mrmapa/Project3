import pygame, sys
from constants import *

def setSearchBar(screen):
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
    searchButton_back.fill(LIGHT_PURPLE)
    searchButton_back_rect = searchButton_back.get_rect(topleft = ((3 * WIDTH)/4 - 8, 13))
    screen.blit(searchButton_back, searchButton_back_rect)

    searchButton = pygame.Surface((50, 32))
    searchButton.fill(LIGHT_PURPLE)
    searchButton_rect = searchButton.get_rect(topleft = ((3 * WIDTH)/4 - 5, 16))
    screen.blit(searchButton, searchButton_rect)

    # search glass

    # search glass handle

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

def main():
    # initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Otakuverse")

    screen.fill([20, 20, 20])

    # loading font
    font = pygame.font.Font("Amazon-Ember-Medium.ttf", 30)

    # loading logo
    logo = pygame.image.load("Otakuverse_logo.png")
    logo = pygame.transform.scale(logo, LOGO_SIZE)

    logo_rect = logo.get_rect(topleft = (10, 10))
    screen.blit(logo, logo_rect)

    # loading search bar
    searchText = font.render("", 0, (120, 120, 120))
    
    setSearchBar(screen)

    # comparable algorithms display
    dfs = font.render("DFS: ", 0, [255, 255, 255])
    bfs = font.render("BFS: ", 0, [255, 255, 255])
    setCompareAlgorithmsBox(dfs, bfs, screen)
    
    # recommended anime display

    forYou = font.render("For You...", 0, [255, 255, 255])
    setRecommendationBox(forYou, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()

if __name__ == "__main__":
    main()