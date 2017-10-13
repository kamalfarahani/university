package dice

import (
	"math"
	"math/rand"
	"os"
	"testing"
	"testing/quick"
	"time"
)

func TestMain(m *testing.M) {
	println("Seeding rand ...")
	rand.Seed(time.Now().UTC().UnixNano())

	exitCode := m.Run()
	os.Exit(exitCode)
}

func TestDice(t *testing.T) {
	diceCheckFunction := func() bool {
		diceNumber := RandDice()
		if diceNumber < 1 || diceNumber > 6 {
			return false
		}

		return true
	}

	CheckQuickWithNillConfig(t, diceCheckFunction)
}

func TestExpectedValueDice(t *testing.T) {
	exCheckFunc := func() bool {
		const expectedValue = float32(3.5)

		diff := math.Abs(float64(AverageDiceValue(100000) - expectedValue))
		if diff > .1 {
			return false
		}

		return true
	}

	CheckQuickWithNillConfig(t, exCheckFunc)
}

func TestToMoney(t *testing.T) {
	for diceNumber, money := range diceToMoney {
		if m, err := ToMoney(diceNumber); m != money && err == nil {
			t.Error("dice number has a wrong money")
		}
	}

	_, err := ToMoney(7)
	if err == nil {
		t.Error("out range number not detected")
	}
}

func CheckQuickWithNillConfig(t *testing.T, checkFunc interface{}) {
	if err := quick.Check(checkFunc, nil); err != nil {
		t.Error(err)
	}
}
