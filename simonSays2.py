from machine import Pin, Timer, PWM
import random, time

randomIntList = []
user_input = []
buzzer = PWM(Pin(17))

leds = [
	Pin(11, Pin.OUT), #Red
	Pin(12, Pin.OUT), #Green
	Pin(13, Pin.OUT), #Blue
	Pin(14, Pin.OUT), #Yellow
	Pin(15, Pin.OUT) #Black
]

buttons = [
	Pin(3, Pin.IN, Pin.PULL_UP), #Red
	Pin(4, Pin.IN, Pin.PULL_UP), #Green
	Pin(5, Pin.IN, Pin.PULL_UP), #Blue
	Pin(6, Pin.IN, Pin.PULL_UP), #Yellow
	Pin(7, Pin.IN, Pin.PULL_UP) #Black
]

def waitForButton():
    now = time.ticks_ms()
    while time.ticks_ms() - now < 3000:
        #time allowance has not expired
        #listen for button presses
        for i in range(len(buttons)):
            if buttons[i].value() == 0: #This means the button is pushed down
                leds[i].value(1)
                while buttons[i].value() == 0:
                    frequency = 800 // (i+1)
                    buzzer.freq(frequency)
                    buzzer.duty_u16(32768)

                buzzer.duty_u16(30)
                time.sleep(0.05)
                leds[i].value(0)
                return i
    return -1

def checkUserInput(): #Makes sure user input matches pattern
    for i in range(len(randomIntList)):
        user_input.append(waitForButton())
        if user_input[i] != randomIntList[i]:
            roundCount()
            randomIntList.clear() #Clear here because game is over
            user_input.clear() #Clear here because game is over
            return
    user_input.clear() #Clear here to prepare list for next comparison

def roundCount(): #Flashes all lights to denote round number
    round_count = 0
    for i in range(len(randomIntList)):
        round_count += 1
    for i in range(round_count): #There's probably a better way to do this
        leds[0].value(1)
        leds[1].value(1)
        leds[2].value(1)
        leds[3].value(1)
        leds[4].value(1)
        buzzer.freq(550)
        buzzer.duty_u16(32768)
        time.sleep(0.4)
        buzzer.duty_u16(0)
        leds[0].value(0)
        leds[1].value(0)
        leds[2].value(0)
        leds[3].value(0)
        leds[4].value(0)
        time.sleep(0.4)
    waitToStart()

def randomLED(): #Generates random LED pattern
    randomLED = random.randint(0,4)
    randomIntList.append(randomLED)
    for i in range(len(randomIntList)):
        time.sleep(0.5)
        leds[randomIntList[i]].value(1)

        frequency = 800 // (randomIntList[i]+1)
        buzzer.freq(frequency)
        buzzer.duty_u16(32768)
        time.sleep(0.5)
        leds[randomIntList[i]].value(0)
        buzzer.duty_u16(0)

def waitToStart(): #Waits for a button push before starting the game
    while True:
        for i in range(len(buttons)):
            if buttons[i].value() == 0:
                return

def loop():
    randomLED()
    checkUserInput()
			
if __name__ == '__main__':
	while True:
		loop()
