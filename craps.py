#Craps Program by Soorya Prasanna Ravichandran

import random #Used for random function.
import copy   #Used to make deep copies.

#Method that will return the sum of the 2 dice rolled.
def getDiceSum():

    int_dice1Value = random.randint(1,6)
    int_dice2Value = random.randint(1,6)

    #Returning the sum of 2 dices.
    return int_dice1Value + int_dice2Value

#Method that will determine if the current game is a win or a loss.
#Returns 1 incase of a Win and 0 incase of a Loss.
def getCurrentGameOutcome():

    #Store the first dice roll outcome.
    int_firstRollSum = getDiceSum()

    #Return the outcome of the current game based on the game rules.
    #If the first outcome is a 7 or 11 then it is a win.
    if int_firstRollSum in [7,11]:
        return 1
    
    #If the first outcome is a 2 or 3 or 12 then it is a loss.
    elif int_firstRollSum in [2,3,12]:
        return 0
    else:
        #Set a loop for other outcomes.
        while True:
            int_diceRollSum = getDiceSum()

            #If the outcome is 7 then it is a loss.
            if int_diceRollSum == 7:
                return 0
                break

            #If any other outcome is equal to the outcome of the first outcome, then it is a win.
            elif int_diceRollSum == int_firstRollSum:
                return 1
                break

#Method that will return the number of times each game lasted and the final amount left.
def runGameEngine(arr_gameResults, int_gameStrategyType):

    #Set the initial amount to $1000.
    int_initialAmount = 1000

    #Copy the value to modify with each win/loss.
    int_currentAmount = copy.deepcopy(int_initialAmount)

    #Initial Wager amount.
    int_wager = 100

    #Game Count
    int_count = 0

    #Set the multiplier of the Wager amount based on the type of Game strategy being used.
    #For Simple Strategy the Wager for win and loss are $100.
    if int_gameStrategyType == 1:
        int_winMultiplier = 1
        int_lossMultiplier = 1
    #For Martingale Strategy the Wager after loss is doubled and after win it remains $100.
    elif int_gameStrategyType == 2:
        int_winMultiplier = 1
        int_lossMultiplier = 2
    #For Anti-Martingale Strategy the Wager after win is doubled and after loss it remains $100.
    elif int_gameStrategyType == 3:
        int_winMultiplier = 2
        int_lossMultiplier = 1

    #Loop to calculate the current balance and the game counts based on the game outcomes.
    for i in arr_gameResults:

        #Check if the balance amount is greater than zero.
        if int_currentAmount > 0:

            #Condition for Win Case.
            if i ==1:
                int_currentAmount += int_wager
                int_wager = calculateWager(int_wager, int_winMultiplier)
                int_count += 1

            #Condition for Loss Case.   
            else:
                int_currentAmount -= int_wager

                #If the wager amount is greater than the balance amount left, then the whole amount becomes wager.
                if calculateWager(int_wager, int_lossMultiplier) > int_currentAmount:
                    int_wager = int_currentAmount
                else:
                    int_wager = calculateWager(int_wager, int_lossMultiplier)
                int_count += 1
        else:
            break
        
    return int_currentAmount, int_count

#Method to calculate the wager amount for the next bet.
def calculateWager(int_currentWager, int_multiplier):
    if int_multiplier == 1:
        return 100
    else:
        return int_currentWager * int_multiplier

#Main Method.             
def main():

    #Initialize the gaming array.
    arr_games = []

    #Maximum number of games will be 10.
    for i in range(10):
        arr_games.append(getCurrentGameOutcome())

    #Play the game for all 3 Strategies and get the balance amount and the number of games played.
    int_balanceForSimple, int_noOfGamesForSimple = runGameEngine(arr_games, 1)
    int_balanceForMartingale, int_noOfGamesForMartingale = runGameEngine(arr_games, 2)
    int_balanceForAntiMartingale, int_noOfGamesForAntiMartingale = runGameEngine(arr_games, 3)

    #Get the Result for all 2 games.
    str_result = "1\t%d\t$%d\n2\t%d\t$%d\n3\t%d\t$%d\n\n" % (int_noOfGamesForSimple, int_balanceForSimple, int_noOfGamesForMartingale, int_balanceForMartingale, int_noOfGamesForAntiMartingale, int_balanceForAntiMartingale)
    return str_result
    
#Method for printing the output to file.       
if __name__ == '__main__':
	import sys
	outp=open('output.txt','w')     #Creating output.csv file for writing the output.

	#Loop to determine the number of rounds to be played and print its output.
	for i in range(5):
		str_output = main()
		outp.write("Round #%d: \n" % (i + 1))
		outp.write("Strategy\t # of Games\t Ending Balance\n")
		outp.write(str_output)
	outp.close()
