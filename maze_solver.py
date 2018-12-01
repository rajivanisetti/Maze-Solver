import requests
import json
import time

directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
directionToMove = {'UP': (0, -1), 'RIGHT': (1,0), 'DOWN': (0,1), 'LEFT': (-1, 0)}
reverseDirections = {'UP': 'DOWN', 'RIGHT': 'LEFT', 'DOWN': 'UP', 'LEFT': 'RIGHT'}

def isValidLocation(move, size):
    return move[0] >= 0 and move[0] < size[0] and move[1] >= 0 and move[1] < size[1]

def getToken():
    return requests.post('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session', {'uid': '904801422'}).json()['token']

def getState(token):
    return requests.get('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + str(token)).json()

def move(token, direction):
    return requests.post('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + str(token), {'action': direction}).json()['result']

def recursiveDFS(token, visited, lastMove):
    currentLoc = getState(token)['current_location']
    print ("Current Location: {}".format(currentLoc))
    size = getState(token)['maze_size']
    x = currentLoc[0]
    y = currentLoc[1]
    visited.add((x, y))

    for direction in directions:
        nextLoc = (x + directionToMove[direction][0], y + directionToMove[direction][1])
        print("Next Attempted Location: {}".format(nextLoc))

        if isValidLocation(nextLoc, size):
            if nextLoc in visited:
                continue
            
            result = move(token, direction)

            if result == 'END':
                print("REACHED THE END OF THE MAZE, HALLELUJAH!")
                return True
            elif result == "SUCCESS":
                correct = recursiveDFS(token, visited, direction)
                if correct:
                    return True
        else:
            continue
            
    print(lastMove)
    print(reverseDirections[lastMove])
    move(token, reverseDirections[lastMove])

    return False

def solve(token):
    visitedLocations = set()
    recursiveDFS(token, visitedLocations, None)

def main():
    token = getToken()
    state = getState(token)

    startTime = time.time()
    accumulatedTime = 0
    mazeNumber = 1

    while state['status'] != 'FINISHED':
        solve(token)
        endTime = time.time()
        accumulatedTime += (endTime - startTime)
        print ("MAZE NUMBER {} FINISHED IN {}".format(mazeNumber, endTime - startTime))
        startTime = time.time()
        mazeNumber += 1
        state = getState(token)
    
    print("FINISHED {} MAZES IN {}".format(mazeNumber, accumulatedTime))




if __name__ == "__main__":
    main()
