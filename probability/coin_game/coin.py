import random


def dropCoin():
    return random.randint(0, 1)


def playCoinGame(gamePrice):
    counter = 0
    while dropCoin() == 0:
        counter += 1

    return (2**(counter + 1) - gamePrice)


def main():
    while True:
        numberOfGames = int(input("Enter number of games : "))
        gamePrice = int(input("Enter game price : "))
        sumOfPrizes = 0

        for i in range(numberOfGames):
            sumOfPrizes += playCoinGame(gamePrice)

        print("Sum of prizes is : ", sumOfPrizes)


if __name__ == "__main__":
    main()
