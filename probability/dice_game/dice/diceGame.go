package dice

import (
	"errors"
	"math/rand"
)

var diceToMoney = map[int]int{
	1: 100,
	2: 400,
	3: 1000,
	4: 2000,
	5: 4000,
	6: 6000,
}

// RandDice Returns a random dice number
func RandDice() int {
	return 1 + rand.Intn(6)
}

// AverageDiceValue calculates the average value of dicing exprimentNumbers times
func AverageDiceValue(exprimentNumbers int) float32 {
	sumOfNumbers := 0
	for i := 0; i < exprimentNumbers; i++ {
		sumOfNumbers += RandDice()
	}

	return float32(sumOfNumbers) / float32(exprimentNumbers)
}

// ToMoney returns amount of money of a random dice number
func ToMoney(diceNumber int) (int, error) {
	if diceNumber > 6 {
		return 0, errors.New("number out of range")
	}

	return diceToMoney[diceNumber], nil
}
