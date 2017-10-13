package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strconv"

	"./dice"
)

const optionsStr = `options:
	1: dice
	2: see average dice number after given expriments number
	3: play for 2750 toman
	4: see average benefit after given games number
	5: clear console
	6: exit
  ----------------------------------------------
`

var optionToFunc = map[int]func(){
	1: doDice,
	2: calculateExprimentAverage,
	3: play,
	4: calculateBenefitAverage,
	5: clearConsole,
	6: exitSuccessfully,
}

var clearConsoleMap = map[string]func(){
	"linux": func() {
		cmd := exec.Command("clear")
		cmd.Stdout = os.Stdout
		cmd.Run()
	},
	"windows": func() {
		cmd := exec.Command("cls")
		cmd.Stdout = os.Stdout
		cmd.Run()
	},
}

func main() {
	for {
		printOptions()
		optionNumber, err := readOption()

		if err != nil {
			panic(err)
		}

		optionToFunc[optionNumber]()
	}
}

func printOptions() {
	fmt.Println(optionsStr)
}

func doDice() {
	fmt.Printf("\n \t dice number : %d \n\n", dice.RandDice())
}

func play() {
	money, _ := dice.ToMoney(dice.RandDice())
	fmt.Printf("\n \t You won : %d \n\n", money)
}

func calculateExprimentAverage() {
	exprimentsNum, err := readInt("Enter number of expriments: ")
	if err != nil {
		return
	}

	fmt.Printf(
		"\n \t average of dice numbers : %f \n\n",
		randAverage(dice.RandDice, exprimentsNum))
}

func calculateBenefitAverage() {
	exprimentsNum, err := readInt("Enter number of expriments: ")
	if err != nil {
		return
	}

	benefitCreatorFunc := func() int {
		money, _ := dice.ToMoney(dice.RandDice())
		return 2750 - money
	}

	fmt.Printf(
		"\n \t average of benefit is : %f \n\n",
		randAverage(benefitCreatorFunc, exprimentsNum))
}

func readOption() (int, error) {
	optionNum, err := readInt("Enter option: ")

	if err != nil {
		return optionNum, err
	}

	if optionNum > 6 {
		return optionNum, errors.New("Option out of range")
	}

	return optionNum, nil
}

func readInt(showTxt string) (int, error) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(showTxt)
	inputStr, _ := reader.ReadString('\n')
	return strconv.Atoi(inputStr[:len(inputStr)-1])
}

func clearConsole() {
	value, ok := clearConsoleMap[runtime.GOOS] //runtime.GOOS -> linux, windows, darwin etc.
	if ok {                                    //if we defined a clear func for that platform:
		value()
	} else { //unsupported platform
		println("Your platform is unsupported! I can't clear terminal screen :(")
	}
}

func exitSuccessfully() {
	os.Exit(0)
}

func randAverage(numCreator func() int, count int) float32 {
	sum := 0
	for i := 0; i < count; i++ {
		sum += numCreator()
	}

	return float32(sum) / float32(count)
}
