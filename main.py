import pygame, sys
from constants import *
from recommender import *
from traversals import *

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

    #### from Mapa-Hupey
    # # loading user rating bar
    # input_rating = 0
    # userRatingBarSetup(font, userRatingFont, screen)
    # inputRating(input_rating, inputRatingFont, screen)

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
