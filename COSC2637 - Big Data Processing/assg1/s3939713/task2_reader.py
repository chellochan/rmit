#!/usr/bin/env python3

from task2_mapper import getMedoids

#check if distance of medoids and medoids_prev have same values
def checkMedoidsDistance(medoids, medoids_prev):
    bool = True
    for idx, medoid in enumerate(medoids):
        if bool:
            bool = ((medoids[idx][0] == medoids_prev[idx][0]) and (medoids[idx][1] == medoids_prev[idx][1]))
        else:
            break

    if bool:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    medoids = getMedoids('medoids.txt')
    medoids_prev = getMedoids('medoids_prev.txt')
    
    checkMedoidsDistance(medoids, medoids_prev)
