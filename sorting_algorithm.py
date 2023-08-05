from copy import copy

# takes in a dictionary where each person has a key (their code) 
# & an integer assigned to them (the number of reliefs they've taken this semester)

# currently working on making it sort the dictionary by int too, might change approach might not
def sort(toSort: dict[str, int]):
    array = list(toSort.values())
    for step in range(1, len(array)):
        key = array[step]
        j = step - 1
        
        # Compare key with each element on the left of it until an element smaller than it is found
        # For descending order, change key<array[j] to key>array[j].        
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j = j - 1
        
        # Place key at after the element just smaller than it.
        array[j + 1] = key

    # work on zipping it back together, returning it and then this should work properly
    unusedNames = list(toSort.keys())
    for name in unusedNames:
        needValue = toSort[name]

    return array