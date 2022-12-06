import pandas as pd
import timeit
#map<string,pair<vector<string>, map<string, int>>

# for both traversals:
# graph is a dictionary with a string and tuple
# the tuple's first element is a list of strings of other usernames
# the tuple's second element is a dictionary containing a string and float
# the string value is the anime name, and float is the rating the CURRENT user gave the anime

def bfs_search(graph, source, user_prefs):
    # get time at start
    start = timeit.default_timer()

    # visited set
    visited = set()

    most_similar_users = {}
    # queue implemented as list
    queue = []

    # source is the username
    visited.add(source)
    queue.append(source)
    while not len(queue) == 0 :
        # set username to first element in the queue and removes it from queue
        username = queue[0]
        queue.pop(0)

        # neighbors is a list, graph[username] is a tuple and 0 is the first element
        neighbors = graph[username][0]

        # neighborUser is a string value from the neighbors list
        for neighborUser in neighbors:

            # check if neighborUser has been visited, if not then add to visited and q
            if neighborUser not in visited:
                visited.add(neighborUser)
                queue.append(neighborUser)

                # calculate similarity between base user and neighborUser
                score = user_prefs[neighborUser]

                # add score to most_similar_users and remove smallest score if necessary
                if (len(most_similar_users) < 20 or score > min(most_similar_users.keys())) and score > 0:
                    most_similar_users[score] = neighborUser
                    if len(most_similar_users) == 21:
                        most_similar_users.pop(min(most_similar_users.keys()))
    similar_users = dict(zip(list(most_similar_users.values()), list(most_similar_users.keys())))
    
    # get time at end
    end = timeit.default_timer()
    time_elapsed = end - start
    return([similar_users, time_elapsed])

def dfs_search(graph, source, user_prefs):
    # get time at start
    start = timeit.default_timer()

    # visited set
    visited = set()

    most_similar_users = {}
    # stack implemented as list
    stack = []

    # source is the username
    visited.add(source)
    stack.append(source)

    while not len(stack) == 0 :
        # set username to first element in the queue and removes it from queue
        username = stack[-1]
        stack.pop()

        # neighbors is a list, graph[username] is a tuple and 0 is the first element
        neighbors = graph[username][0]

        # neighborUser is a string value from the neighbors list
        for neighborUser in neighbors:

            # check if neighborUser has been visited, if not then add to visited and q
            if neighborUser not in visited:
                visited.add(neighborUser)
                stack.append(neighborUser)

                # calculate similarity between base user and neighborUser
                score = user_prefs[neighborUser]

                # add score to most_similar_users and remove smallest score if necessary
                if (len(most_similar_users) < 20 or score > min(most_similar_users.keys())) and score > 0:
                    most_similar_users[score] = neighborUser
                    if len(most_similar_users) == 21:
                        most_similar_users.pop(min(most_similar_users.keys()))
    similar_users = dict(zip(list(most_similar_users.values()), list(most_similar_users.keys())))
    
    # get time at end
    end = timeit.default_timer()
    time_elapsed = end - start
    return([similar_users, time_elapsed])