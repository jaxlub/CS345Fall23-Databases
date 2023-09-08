def join(r1: set, r2: set):
    # cross product of two relations
    result = set()
    for (name, id1) in r1:
        for (id2, course) in r2:
            if id1 == id2:
                result.add((id1, name, course))
    return result


# if we are executing this file directly and not being imported by another python file
# then run this code
if __name__ == "__main__":
    # python implements sets as efficiently as hash tab;e
    students = {('Harry', 1), ('Ron', 3), ('Hermione', 2), ('Draco', 666)}
    enrollments = {('1,', 'P101'), ('2', 'DA101'), ('1', 'DA101'), ('3', 'P101')}
    
    print(join({1, 2, 3}, {'a', 'b', 'c'}))  # expect 12
    print(join(students, enrollments))
