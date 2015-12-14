# Name:         :    VenkataSatya
# E-Mail:       :    vyenugu@student.fitchburgstate.edu
# Student ID    :    @01311701

# Partner Name  :    Srikanth Reddy Ega
# Partner Email :    sega@student.fitchburgstate.edu  
# Partner ID    :    @01314250

# Partner Name  :    Kofi Kyei
# Partner Email :    kkyei@student.fitchburgstate.edu
# Partner ID    :    @01263131

# Final Project 
# Description   :    Program which predicts the movies and searches the movies from the dataset.
# Bugs          :    None

# Note          :    Kindly run the program in Canopy.


import random
import operator
import numpy as np
import matplotlib.pyplot as plt


def read_movies_file(fileName):
    Movie_Dict ={}
    file = open(fileName,"r")
    count = 0
    generics_dict = {}
    for line in file:
        count += 1
        if(count == 1):
            continue
        elements = []
        line = line.strip()
        elements.append(line[:line.find(',')])
        elements.append(line[line.find(',')+1 : line.rfind(',')])
        if(elements[1].find(",") != -1):
            elements[1] = elements[1][1:-1]
        elements.append(line[line.rfind(',')+1:].split('|'))
        for generics in elements[2]:
            if(generics not in generics_dict):
                generics_dict[generics] = 1
            else:
                generics_dict[generics] += 1
        Movie_Dict[int(elements[0])] = elements
    return Movie_Dict, generics_dict


def read_ratings_file(fileName, Movie_Dict):
    file = open(fileName,"r")
    temp_dict = dict()
    count = 0
    for line in file:
        count += 1
        if(count == 1):
            continue
        line = line.strip()
        elements = line.split(",")
        if elements[1] in temp_dict:
            temp_dict[elements[1]].append(int(elements[2]))
        else:
            temp_dict[elements[1]] = [int(elements[2])]
    rating_count = {}
    for key, value in temp_dict.items():
        count = len(value)
        rating_count[int(key)] = sum(value)/count,count
    avg_ratings_list = {}
    avg_ratings_list = sorted(rating_count.items(), key=operator.itemgetter(1))
     # This loop code will make the unrated movies by user to user rating as 0 and number of user rated as 0 
    for key in Movie_Dict.keys():
        if(key not in  rating_count.keys()):
            rating_count[key] =(0,0)
    return rating_count, avg_ratings_list


def prediction_liking(Movie_Dict, generics_dict, avg_ratings_list):
    user_choice_generics_dict = {}
    counter = 0
    numbers = []
    print "\n"
    while(True):                
        options_dict ={}
        count = 0
        for i in range(4):
            movie_id = random.randint(1,3882)
            if ((movie_id in numbers) or (movie_id not in Movie_Dict.keys())):
                movie_id = random.randint(1,3882)
            numbers.append(movie_id)
            print "(",i+1,")",Movie_Dict[movie_id][1],"\t"
            options_dict[i+1] = movie_id
            count += 1
            if(count == 4):
                choice = raw_input("\nPlease select the movie which you like \n\t\t(or)\ntype anything else to skip : ")
                if(choice != ''):
                    try:
                        choice = int(choice)
                    except ValueError:
                        print("\nYou have select an invalid option, so the question got skipped\n")
                        continue
                else:
                    print "\nYou have select an invalid option, so the question got skipped\n"
                    continue
                print
                if(choice in options_dict):
                    counter += 1
                    for choice_generics in Movie_Dict[options_dict[choice]][2]:
                        if(choice_generics not in user_choice_generics_dict):
                            user_choice_generics_dict[choice_generics] = 1
                        else:
                            user_choice_generics_dict[choice_generics] += 1
                else:
                    print "\nYou have select an invalid option, so the question got skipped\n"
        if(counter == 5):
            break
        else:
            continue
        
    maximum = 0
    like_list = []
    prediction_liking_graph_using_generics(user_choice_generics_dict)
    for generic_count in user_choice_generics_dict:
        if(user_choice_generics_dict[generic_count] > maximum):
            maximum = user_choice_generics_dict[generic_count]
            like_list = [generic_count]
        elif(user_choice_generics_dict[generic_count] == maximum):
            like_list.append(generic_count)
    if(len(like_list) != 0):
        print "Our Prediction program says that you like", like_list, "movies more, so below are the top 20 movies in that generic."
        for like in like_list:
            print "\nSo the top 20 ",like," movies as per user ratings are:\n"
            top20movies1(Movie_Dict, generics_dict, avg_ratings_list, like)
        print "\nKindly find the Graph in the current working directory with file name User_Ratings_Generics.png"
        print "\nHope you will see and enjoy..!!!\n"
        print "=======================================================================================================================\n"
        
    else:
        print "You have skipped all the questions"
    

def prediction_liking_graph_using_generics(user_choice_generics_dict):
    generics = (user_choice_generics_dict.keys())
    y_pos = np.arange(len(generics))
    ratings = user_choice_generics_dict.values()
    fig = plt.figure()
    plt.barh(y_pos, ratings, align='center')
    plt.yticks(y_pos, generics)
    plt.xlabel('Generes')
    plt.title('The chart shows the ratings you\'ve provided in each movie genre.\n Movies may belong to multiple genres.')
    fig.savefig('User_Ratings_Generics.png')
    #plt.show()
    

    
def top20movies(Movie_Dict, generics_dict, avg_ratings_list):
    for element in generics_dict:
        print "\n{:10s}".format(element),"\t"
    choice = input("\n \nPlease enter the generic from the above list by which you want to search the top20 movies rated: ")
    print()
    top20movies1(Movie_Dict,generics_dict, avg_ratings_list, choice)


def top20movies1(Movie_Dict, generics_dict, avg_ratings_list, choice):
    count = 0
    temp_dict = reversed(avg_ratings_list)
    print "{:90s}{:25s}{:7s}".format("Title", "Avg Rating", "Number of user rated")
    for element in temp_dict:
        if(count < 20):
            if choice in Movie_Dict[element[0]][2] and element[1][1] > 10:
                count += 1
                print "{:77s}".format(Movie_Dict[element[0]][1]), "{:20d}".format(element[1][0]), "{:25d}".format(element[1][1])
        else:
            break


def Rating_Prediction(Movie_Dict, generics_dict, avg_ratings_list):
    count = 0
    numbers = []
    Rating = {}
    while(count<5):
        movie_id = random.randint(1,3882)
        if ((movie_id in numbers) or (movie_id not in Movie_Dict.keys())):
            movie_id = random.randint(1,3882)
        numbers.append(movie_id)        
        print "\nPlease rate the movie: ",Movie_Dict[movie_id][1] 
        User_Input_Rating = raw_input("Please rate the movie prompted in range(1-5) \n\t\t(or)\ntype anything else to skip: ")
        if(User_Input_Rating != ''):
                    try:
                        User_Input_Rating = float(User_Input_Rating)
                    except ValueError:
                        print("\nYou have select an invalid option, so the question got skipped\n")
                        continue
        else:
            print "\nYou have select an invalid option, so the question got skipped\n"
            continue
        print
        if(User_Input_Rating <= 5.0 and  User_Input_Rating >= 0.0):
            count += 1           
            for movie in avg_ratings_list:
                if(movie[0] == movie_id):
                    Rating[movie[0]]=[float(User_Input_Rating),movie[1][0],movie[0]]

        else:
            print "You have entered an invalid option, so the question got skipped"
            continue
    for key, element in Rating.items():
        if(element[0] > element[1]):
            print "You have rated",element[0],"for",Movie_Dict[element[2]][1],"which is more than  the average rating(",element[1],") given to it by the users"
        elif(element[0] < element[1]):
            print "You have rated",element[0],"for",Movie_Dict[element[2]][1],"which is less than  the average rating(",element[1],") given to it by the users"
        elif(element[0] == element[1]):
            print "You have rated",element[0],"for",Movie_Dict[element[2]][1],"which is equal  the average rating(",element[1],") given to it by the users"
    
    user_genric_dict_final = Rating_Prediction_graph(Rating) 
    maximum = 0
    like_list = []
    for generic_count in user_genric_dict_final:
        if(user_genric_dict_final[generic_count] > maximum):
            maximum = user_genric_dict_final[generic_count]
            like_list = [generic_count]
        elif(user_genric_dict_final[generic_count] == maximum):
            like_list.append(generic_count)
    if(len(like_list) != 0):
        print "\nOur Prediction program says that you like", like_list, "movies more, so below are the top 20 movies in that generic."
        for like in like_list:
            print "\nSo the top 20 ",like," movies as per user ratings are:\n"
            top20movies1(Movie_Dict, generics_dict, avg_ratings_list, like)
        print "\nKindly find the Graph in the current working directory with file name User_Ratings.png"
        print "\nHope you will see and enjoy..!!!\n"
        print "=======================================================================================================================\n"

    else:
        print "You have skipped all the questions"       
 

def Rating_Prediction_graph(Rating):
    user_genric_dict ={}
    user_genric_dict_final = {}
    for key, element in Rating.items():
        temp = Movie_Dict[element[2]]
        temp1 = temp[2]
        for generics in temp1:
            if(generics not in user_genric_dict):
                user_genric_dict[generics] = [element[0],1]
            else:
                user_genric_dict[generics] = [user_genric_dict[generics][0]+element[0], user_genric_dict[generics][1]+1]
    for key,value in user_genric_dict.items():
        user_genric_dict_final[key] = value[0]/value[1]
    generics = (user_genric_dict_final.keys())
    y_pos = np.arange(len(generics))
    ratings = user_genric_dict_final.values()
    fig = plt.figure()
    plt.barh(y_pos, ratings, align='center')
    plt.yticks(y_pos, generics)
    plt.xlabel('Ratings avarages for each generic')
    plt.title('The chart shows the average ratings you\'ve provided for each generic')
    fig.savefig('User_Ratings.png')
    #plt.show()
    return user_genric_dict_final
        
        
def Search_Movies_BY_Year(Movie_Dict, rating_count):
    year_list = {}
    for i in Movie_Dict.keys():
        year = Movie_Dict[i][1][Movie_Dict[i][1].rfind('(')+1 : Movie_Dict[i][1].rfind(')')]
        year = int(year)
        if(year not in year_list.keys()):
            year_list[year] = [[Movie_Dict[i][1], rating_count[i][0], rating_count[i][1]]]
           
        else:
            for key in year_list.keys():
                if(key == year):
                    year_list[key].append([Movie_Dict[i][1], rating_count[i][0], rating_count[i][1]])
    return year_list
    

def Search_Movies_BY_Generic(Movie_Dict, generic, rating_count):
    user_generic_list = []
    for key,value in Movie_Dict.items():
        if(generic.lower() in str(Movie_Dict[key][2]).lower()):
            user_generic_list.append([Movie_Dict[key][1], rating_count[key][0], rating_count[key][1]])        
    return user_generic_list


def Search_Movies_BY_Rating(Movie_Dict, avg_ratings_list, rating):
    temp_list = reversed(avg_ratings_list)
    print "\nMovies with given rating are:\n"
    print "{:90s}{:25s}{:7s}".format("Title", "Avg Rating", "Number of user rated")
    for element in temp_list:
        if element[1][0] == rating:
            print "{:77s}".format(Movie_Dict[element[0]][1]), "{:20d}".format(element[1][0]), "{:25d}".format(element[1][1])
    return
                
    
def Search_Movies_BY_Name(Movie_Dict, rating_count, movie_name):
    flag = 0
    for key,value in Movie_Dict.items():
        temp_movie = value[1]
        index = temp_movie.find("(")
        temp_movie = temp_movie[:index-1]
        if(movie_name.lower() in str(value).lower() or temp_movie.lower() == movie_name.lower()):
            print "\nMovie:", Movie_Dict[key][1], "\nThe average rating is:", rating_count[key][0], "\nNumber of people rated are:", rating_count[key][1]
            print "\nHope you will see and enjoy.\n"
            flag = 1
            break   
    if(flag == 0):
        print "\nMovie not found in our dataset. We are sorry.\n"
    return


print "\n\t\t\t======================================================"
print "\t\t\tWelcome to Movie Prediction and Movies Search Program "
print "\t\t\t======================================================\n"
while(True):
    Movie_Dict = {}
    Movie_Dict, generics_dict = read_movies_file("Movies_Final.csv")
    rating_count, avg_ratings_list = read_ratings_file("Ratings_Final.csv", Movie_Dict)    
    print "  1. Prediction of Movies you might Like by answering which movies your like from given movies choice"
    print "  2. Prediction of Movies you might Like using Rating given by you for the given movie"
    print "  3. Search Movies by Year"
    print "  4. Search Movies by Generics"
    print "  5. Search Movies by Rating"
    print "  6. Search Movies by Name"
    print "  7. Quit" 
    choice = raw_input("Please enter your choice from above menu: ")
    if(choice == '1'):
        prediction_liking(Movie_Dict, generics_dict, avg_ratings_list)
        continue
    if(choice == '2'):
        Rating_Prediction(Movie_Dict, generics_dict, avg_ratings_list)
        continue
    if(choice == '3'):
        year_dict = Search_Movies_BY_Year(Movie_Dict, rating_count)
        year = raw_input("Please enter the Year: ")
        if(year != ''):
            try:
                year = int(year)
            except ValueError:
                print("\nYou have given an invalid format for the year,  Try Again...!!\n")
                continue
        else:
            print "\nYear can not be blank. Try Again...!!\n"
            continue
        if(year in year_dict.keys()):
            print "\nMovies found in the dataset for the year", year, "are:\n"
            print "{:90s}{:25s}{:7s}".format("Title", "Avg Rating", "Number of user rated")
            temp_list = year_dict[year]
            for index in range(len(temp_list)):
                print "{:77s}".format(temp_list[index][0]), "{:20d}".format(temp_list[index][1]), "{:25d}".format(temp_list[index][2])
            print "\nHope you will see and enjoy.\n"
        else:
            print "\nNo Movies in the given years with in our dataset\n"
        continue
    if(choice == '4'):
        print "\n", generics_dict.keys()
        generic = raw_input("Please enter the generic from the above list, Example:'Darma' :")
        if(generic.lower() in  str(generics_dict.keys()).lower()):
            user_generic_list = Search_Movies_BY_Generic(Movie_Dict, generic, rating_count)
            print "\nMovies found in the dataset for the", generic, "generic are:\n"
            print "{:90s}{:25s}{:7s}".format("Title", "Avg Rating", "Number of user rated")
            for i in range(len(user_generic_list)):
                print "{:77s}".format(user_generic_list[i][0]), "{:20d}".format(user_generic_list[i][1]), "{:25d}".format(user_generic_list[i][2])
            print "\nHope you will see and enjoy.\n"
        else:
            print "\nGiven generic is Invalid\n"   
        continue
    if(choice == '5'):
        rating = raw_input("Please enter the rating in interger(Range of 1-5): ")
        if(rating != ''):
            try:
                rating = int(rating)
            except ValueError:
                print("\nYou have given an invalid format for the rating,  Try Again...!!\n")
                continue
        else:
            print "\nRating can not be blank. Try Again...!!\n"
            continue
        if(rating in range(1,6)):
            Search_Movies_BY_Rating(Movie_Dict, avg_ratings_list, rating)
            print "\nHope you will see and enjoy.\n"
        else:
            print "\nInvalid Rating\n"
        continue
    if(choice == '6'):
        movie_name = raw_input("Please enter the movie name: ")
        Search_Movies_BY_Name(Movie_Dict, rating_count, movie_name)
        continue
    if(choice == '7'):
        break
    else:
        print "\nInvalid choice. Try Again...!!!\n"
        continue
print "\nThank you once again for using our program. Hope you have enjoyed using it...!!"
