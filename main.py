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

    # search text
    if input == "":
        searchText = font.render("Search...", False, (120, 120, 120))
    else:
        searchText = font.render(input, False, (120, 120, 120))
    screen.blit(searchText, searchBar_rect)

def insertionStatus(input, anime_list, input_rating):
    status = ""
    if (input not in anime_list):
        status = "Anime not found."
    elif (input_rating == 0):
        status = "Anime not rated."
    else:
        status = input + " added successfully!"

    return status

def insertionStatusVisual(status, font, screen):
    status_surface = pygame.Surface((300, 100))
    status_rect = status_surface.get_rect(topleft = (450, 150))
    status_text = font.render(status, False, [255, 255, 255])
    status_surface.fill([50, 50, 50])
    status_surface.blit(status_text, (35, 40))
    screen.blit(status_surface, status_rect)

def setRecommendationBox(forYou, screen):
    new_rec = pygame.Surface((600, 600))
    new_rec.fill([70, 70, 70])
    new_rec_rect = new_rec.get_rect(topleft = (WIDTH - 600, 100))
    screen.blit(new_rec, new_rec_rect)

    for i in range(0, 5):
        pygame.draw.line(screen, [20, 20, 20], (WIDTH - 600, 100 + 120 * (i + 1)), (WIDTH, 100 + 120 * (i + 1)), 4)
    
    forYou_rect = forYou.get_rect(center = (WIDTH - 300, 75))
    screen.blit(forYou, forYou_rect)

def setRecommendationsInBox(rec_animes, font, screen):
    for i in range (0, 5):
        recSurface = pygame.Surface((200, 60))
        recSurface_rect = recSurface.get_rect(center = (WIDTH-475, 60 + 120 * (i+1)))
        recText = font.render(rec_animes[i], False, (255, 255, 255))
        recSurface.fill([70, 70, 70])
        screen.blit(recSurface, recSurface_rect)
        screen.blit(recText, recSurface_rect)

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
    generateTextFont = pygame.font.Font("Amazon-Ember-Medium.ttf", 40)
    statusTextFont = pygame.font.Font("Amazon-Ember-Medium.ttf", 20)
    instructionTextFont = pygame.font.Font("Amazon-Ember-Medium.ttf", 15)

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

    # generate button
    generateButton = pygame.Surface((300, 150))
    generateButton_rect = generateButton.get_rect(center = (600, 400))
    generateButton.fill(PURPLE)
    generateText = generateTextFont.render("GENERATE", False, [255, 255, 255])
    generateButton.blit(generateText, (50, 55))

    # instructions visuals
    instructions_surface = pygame.Surface((400, 500))
    instructions_rect = instructions_surface.get_rect(topleft = (0,100))
    instruction_text1 = instructionTextFont.render("How to use:", False, [255, 255, 255])
    instruction_text2 = instructionTextFont.render("Step 1. Input an anime title in the search bar", False, [255, 255, 255])
    instruction_text3 = instructionTextFont.render("Step 2. Rate your anime using the buttons below", False, [255, 255, 255])
    instruction_text4 = instructionTextFont.render("Step 3. Hit enter and repeat steps 1 and 2 until satisfied", False, [255, 255, 255])
    instruction_text5 = instructionTextFont.render("Step 4. Click the Generate button", False, [255, 255, 255])
    instruction_text6 = instructionTextFont.render("Step 5. Enjoy your new favorite anime!", False, [255, 255, 255])
    instructions_surface.fill((20, 20, 20))
    instructions_surface.blit(instruction_text1, (0, 0))
    instructions_surface.blit(instruction_text2, (0, 20))
    instructions_surface.blit(instruction_text3, (0, 40))
    instructions_surface.blit(instruction_text4, (0, 60))
    instructions_surface.blit(instruction_text5, (0, 80))
    instructions_surface.blit(instruction_text6, (0, 100))

    #### from Mapa-Hupey
    # loading user rating bar
    input_rating = 0
    userRatingBarSetup(font, userRatingFont, screen)
    inputRating(input_rating, inputRatingFont, screen)

    # load list of animes
    anime_list = pd.read_csv("anime_data/AnimeListTrimmed.csv", usecols=['anime_id', 'title', 'image_url', 'genre'],
        dtype={'anime_id': int, 'title': str, 'image_url': str, 'genre': str})
    anime_list = set(anime_list['title'])
    
    user_rated_animes = []
    user_ratings = []
    rec_animes = []
    status = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                elif event.key == pygame.K_RETURN:
                    if input in anime_list and input_rating != 0:
                        user_rated_animes.append(input)
                        user_ratings.append(input_rating)
                    else:
                        print("ERROR: Insertion not successful.")

                    status = insertionStatus(input, anime_list, input_rating)
                    print(status)
                    input = ""
                    input_rating = 0
                else:
                    input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (0 <= pygame.mouse.get_pos()[0] <= 1000 and
                    HEIGHT-100 <= pygame.mouse.get_pos()[1] <= HEIGHT):
                        input_rating = (pygame.mouse.get_pos()[0] // 100) + 1
                elif generateButton_rect.collidepoint(event.pos):
                    if (len(user_rated_animes) == 0):
                        print("Error: No animes rated.")
                        continue
                    user_prefs_df = create_user_df(user_rated_animes, user_ratings)

                    similarity_matrix, anime_scores = similarity_matrix_generator(user_prefs_df)
                    similarity_matrix = similarity_matrix.iloc[: , :-1]
                    user_similarities = similarity_matrix.loc['sample_base_user']
                    if (user_similarities.isna().sum() == len(user_similarities)):
                        print("Warning: Not enough user data to produce accurate results.")
                    similarity_matrix = similarity_matrix.iloc[:-1, :]

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
                    # search the graph using DFS and BFS
                    most_similar_users_1, bfs_time = bfs_search(similarity_graph, '-Ackerman', user_similarities)
                    most_similar_users_2, dfs_time = dfs_search(similarity_graph, '-Ackerman', user_similarities)
                    bfs_time = bfs_time * 1000
                    bfs_time = round(bfs_time, 3)
                    dfs_time = dfs_time * 1000
                    dfs_time = round(dfs_time, 3)
                    dfs = font.render("DFS: " + str(dfs_time) + "ms", False, [255, 255, 255])
                    bfs = font.render("BFS: " + str(bfs_time) + "ms", False, [255, 255, 255])
                    # create list of 5 recommended animes
                    rec_animes = anime_recommender(user_rated_animes, most_similar_users_1, similarity_graph)
                    print(rec_animes)

            screen.fill((20, 20, 20))
            setSearchBar(searchText, input, font, screen)
            setRecommendationBox(forYou, screen)
            setCompareAlgorithmsBox(dfs, bfs, screen)
            userRatingBarSetup(font, userRatingFont, screen)
            inputRating(input_rating, inputRatingFont, screen)
            screen.blit(logo, logo_rect)
            screen.blit(generateButton, generateButton_rect)
            if (len(rec_animes) > 0):
                setRecommendationsInBox(rec_animes, inputRatingFont, screen)
            screen.blit(instructions_surface, instructions_rect)
            insertionStatusVisual(status, statusTextFont, screen)

            pygame.display.update()

if __name__ == "__main__":
    main()
