import pygame, sys
from constants import *
from recommender import *
from traversals import *

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

    # user_rated_animes: list of animes that user has rated
    # user_rating: list of corresponding scores
    user_rated_animes = ['Neon Genesis Evangelion', 'Death Note', 'Hunter x Hunter (2011)', 'Monster', 'Death Parade'] #TODO: change this to take input
    user_ratings = [7.0, 6.0, 9.0, 2.0, 4.0] # TODO: change this to take input
    user_prefs_df = create_user_df(user_rated_animes, user_ratings)
    
    similarity_matrix, anime_scores = similarity_matrix_generator(user_prefs_df)
    similarity_matrix = similarity_matrix.iloc[: , :-1]
    user_similarities = similarity_matrix.loc['sample_base_user']
    similarity_matrix = similarity_matrix[0:1000]

    # creating graph without user-input data
    similarity_graph = {}
    for user in similarity_matrix.index:
        # finding the 20 users with the closest similarity scores
        currUser = similarity_matrix.loc[:, user]
        sortedSims = currUser.sort_values(ascending=False)[0:20]
        adjacentUsers = set(sortedSims.index)

        # finding the top 20 highest-rated animes by user
        userPrefs = anime_scores.loc[user].sort_values(ascending=False)[0:20]
        scores = list(userPrefs.values)
        animes = list(userPrefs.index)

        # inserting animes / ratings into a dictionary
        animePrefs = dict(zip(animes, scores))

        # creating tuple of adjacentUsers and a user's anime preferences
        value = (adjacentUsers, animePrefs)
    
        similarity_graph[user] = value
    # making the graph bidirectional
    for user in similarity_graph.keys():
        for adjacentUser in similarity_graph[user][0]:
            similarity_graph[adjacentUser][0].add(user)
    
    print("Starting BFS")
    most_similar_users, bfs_time = bfs_search(similarity_graph, '-Ackerman', user_similarities)
    print(most_similar_users)
    
    print("Starting DFS")
    most_similar_users, dfs_time = dfs_search(similarity_graph, '-Ackerman', user_similarities)
    print(most_similar_users)

    print(bfs_time, dfs_time)

    rec_animes = anime_recommender(user_rated_animes, most_similar_users, similarity_graph)
    print(rec_animes)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main()