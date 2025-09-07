# imports
import turtle as trtl
import random
import time
import pygame

#---------------------------------------------INITIALIZE-----------------------------------------

# initialize pygame mixer for sound effects
pygame.init()
pygame.mixer.init()

# create screen
wn = trtl.Screen()
wn.setup(width = 1000, height = 800)
wn.bgpic("background.gif")

# initializing variables
letters = list("abcdefghijklmnopqrstuvwxyz")
typedLetter = ''
score = 0
colors = ["red", "SeaGreen2", "green", "orange", "purple", "gold", "darkred", "CadetBlue2", "lime", "salmon", "indigo", "brown", "pink", "magenta", "maroon", 'aquamarine']
playerNames = []
playerScores = []
playerName = ''
gameon = None
restart = None
modifier = 1
leftPressed = False
rightPressed = False
playerShootCooldown = 0
totalAmmo = 6
laserAlienMap = []
gameMode = None
difficulty = None
currentLoop = None
loopId = 0

# sound effects
laserSFX = pygame.mixer.Sound("laser sfx.mp3")
explosionSFX = pygame.mixer.Sound("explosion.mp3")
shipSFX = pygame.mixer.Sound("spaceship.mp3")
clickSFX = pygame.mixer.Sound("button click.mp3")
menuSound = pygame.mixer.Sound("menu.wav")
startSFX = pygame.mixer.Sound("game start.mp3")
typingbackgroundSFX = pygame.mixer.Sound("typing background.wav")
arrowbackgroundSFX = pygame.mixer.Sound("arrow background.wav")
loseSFX = pygame.mixer.Sound("game end.mp3")

explosionSFX.set_volume(0.2)
laserSFX.set_volume(0.2)
clickSFX.set_volume(0.4)
menuSound.set_volume(0.7)
startSFX.set_volume(2)
typingbackgroundSFX.set_volume(1.2)
arrowbackgroundSFX.set_volume(0.5)
loseSFX.set_volume(0.7)

# gamemode variables
arrowPlayerMode = None
rampUpMode = None
typingMode = None

easyMode = None
mediumMode = None
hardMode = None

# speed variables
alienSpeed = None
playerSpeed = None
playerSpeed = None
laserSpeed = None

# target lineup and various event control variables
targetLineup = []
currentTarget = None
movingToTarget = False
firingLaser = False

# adding graphics to screen
alienGraphics = ['alienship1.gif', 'alienship2.gif', 'alienship3.gif']
for graphic in alienGraphics + ['player ship.gif', 'laser.gif', 'start button.gif', 'exit button.gif', 'easy button.gif', 'medium button.gif', 'hard button.gif', 'arrow mode button.gif',
                                'typing mode button.gif', 'ramp up mode button.gif', 'start button pressed.gif', 'exit button pressed.gif', 'easy button pressed.gif', 'medium button pressed.gif',
                                'hard button pressed.gif', 'arrow mode button pressed.gif', 'typing mode button pressed.gif', 'ramp up mode button pressed.gif']:
    wn.addshape(graphic)

# alien and laser list
aliens = []
lasers = []

# create all turtles
wn.tracer(False)

player = trtl.Turtle()
scoreTurt = trtl.Turtle()
laserTurt = trtl.Turtle()
startTurt = trtl.Turtle()
writeTurt = trtl.Turtle()
menuPlayer = trtl.Turtle()
menuAlien1 = trtl.Turtle()
menuAlien2 = trtl.Turtle()
menuLaser = trtl.Turtle()
dottedLine = trtl.Turtle()
startButton = trtl.Turtle()
restartButton = trtl.Turtle()
easyButton = trtl.Turtle()
mediumButton = trtl.Turtle()
hardButton = trtl.Turtle()
arrowModeButton = trtl.Turtle()
typingModeButton = trtl.Turtle()
rampUpModeButton = trtl.Turtle()

wn.tracer(True)

shipSFX.play(-1)

#-------------------------------------FUNCTIONS------------------------------------

# all the initializtion of turtles
def initTurtles():
    wn.tracer(False)
    # create the alien and laser turtles
    for i in range(4):
        alien = trtl.Turtle()
        alien.up()
        alien.speed(0)
        alien.ht()
        alien.shape(random.choice(alienGraphics))
        alien.color(random.choice(colors))
        aliens.append(alien)

        
        if not(arrowPlayerMode):
            # laser turtle
            laser = trtl.Turtle()
            laser.up()
            laser.speed(0)
            laser.ht()
            laser.shape('laser.gif')
            lasers.append(laser)

    # initalizing all other turtles
    player.speed(0)
    player.up()
    player.goto(0, -350)
    player.shape('player ship.gif')
    player.ht()

    scoreTurt.up()
    scoreTurt.speed(0)
    scoreTurt.ht()


    laserTurt.up()
    laserTurt.speed(0)
    laserTurt.shape('laser.gif')
    laserTurt.ht()

    startTurt.ht()
    startTurt.up()

    writeTurt.speed(0)
    writeTurt.ht()
    writeTurt.up()

    menuPlayer.up()
    menuPlayer.speed(0)
    menuPlayer.goto(0, -200)

    dottedLine.ht()
    dottedLine.width(3)

    startButton.speed(0)
    startButton.up()
    startButton.goto(0,50)
    startButton.shape('start button.gif')
    startButton.ht()

    restartButton.shape('exit button.gif')
    restartButton.ht()
    restartButton.speed(0)
    restartButton.up()

    easyButton.up()
    easyButton.speed(0)
    easyButton.shape('easy button.gif')
    easyButton.ht()

    mediumButton.up()
    mediumButton.speed(0)
    mediumButton.shape('medium button.gif')
    mediumButton.ht()

    hardButton.up()
    hardButton.speed(0)
    hardButton.shape('hard button.gif')
    hardButton.ht()

    arrowModeButton.up()
    arrowModeButton.speed(0)
    arrowModeButton.shape('arrow mode button.gif')
    arrowModeButton.ht()

    typingModeButton.up()
    typingModeButton.speed(0)
    typingModeButton.shape('typing mode button.gif')
    typingModeButton.ht()

    rampUpModeButton.up()
    rampUpModeButton.speed(0)
    rampUpModeButton.shape('ramp up mode button.gif')
    rampUpModeButton.ht()

    startButton.goto(0,0) 

    typingModeButton.goto(-370, 50)
    arrowModeButton.goto(-370, -50)
    rampUpModeButton.goto(0, -300)

    easyButton.goto(370, 100)
    mediumButton.goto(370, 0)
    hardButton.goto(370, -100)

    wn.tracer(True)

# show the menu screen
def showMenu():
    # reset variables for restarting game
    global gameon, score, restart
    gameon = False
    restart = False
    score = 0

    # reset, hide, and show appropriate turtle
    for alien in aliens:
        alien.ht()
        alien.clear()

    for laser in lasers:
        laser.ht()

    dottedLine.clear()
    player.ht()
    scoreTurt.clear()
    writeTurt.clear()

    menuAlien1.st()
    
    # show appropriate buttons
    if not rampUpMode:
        easyButton.st()
        mediumButton.st()
        hardButton.st()
    arrowModeButton.st()
    typingModeButton.st()
    rampUpModeButton.st()

    restartButton.ht()

    wn.tracer(False)
    # hide start button if no gamemode is selected
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # start button
    startTurt.up()
    startTurt.speed(0)
    startTurt.goto(0, 250)
    startTurt.color(random.choice(colors))
    startTurt.write("Welcome to Space Defender!!!!", font = ["Minecraft", 40, "normal"], align = "center")
    startTurt.color(random.choice(colors))
    startTurt.goto(350, -300)
    startTurt.write("By Sohm Shah", font = ["Minecraft", 20, "normal"], align = "center")
    startTurt.goto(0,50)
    startTurt.color(random.choice(colors))
    
    # menu player animation
    menuPlayer.st()
    menuPlayer.shape('player ship.gif')

    # the 2 aliens in the menu
    menuAlien1.speed(0)
    menuAlien1.up()
    menuAlien1.shape(random.choice(alienGraphics))
    menuAlien1.goto(-200, 150)

    menuAlien2.speed(0)
    menuAlien2.up()
    menuAlien2.shape(random.choice(alienGraphics))
    menuAlien2.goto(200, 150)
    menuAlien2.ht()

    menuLaser.speed(0)
    menuLaser.up()
    menuLaser.shape('laser.gif')
    menuLaser.ht()

    movingLeft = True

    # start screen animation
    while not(gameon):
        # moving left
        if movingLeft:

            # shoot laser and change directions
            if (menuPlayer.xcor() - -200) < -10:
                menuAlien2.shape(random.choice(alienGraphics))
                menuAlien2.st()
                laserSFX.play()
                menuLaser.goto(menuPlayer.xcor(), menuPlayer.ycor())
                menuLaser.st()
                while(menuLaser.ycor() < 125):
                    menuLaser.goto(menuLaser.xcor(), menuLaser.ycor() + 15)
                
                explosionSFX.play()
                movingLeft = False
                menuLaser.ht()
                menuAlien1.ht()
                continue

            menuPlayer.goto(menuPlayer.xcor() - 5, menuPlayer.ycor())
        #moving right
        else:
            # shoot laser and change directiosn
            if (menuPlayer.xcor() - 200) > 10:
                laserSFX.play()
                menuAlien1.shape(random.choice(alienGraphics))
                menuAlien1.st()
                movingLeft = True
                menuLaser.goto(menuPlayer.xcor(), menuPlayer.ycor())
                menuLaser.st()
                while(menuLaser.ycor() < 125):
                    menuLaser.goto(menuLaser.xcor(), menuLaser.ycor() + 15)
                
                explosionSFX.play()
                menuLaser.ht()
                menuAlien2.ht()
                continue

            menuPlayer.goto(menuPlayer.xcor() + 5, menuPlayer.ycor())

    #v initalize and start the game
    menuSound.stop()
    gameStart()

# click function to start the game
def whenClicked(x,y):
    global gameon

    clickSFX.play()

    startButton.shape('start button pressed.gif')
    time.sleep(0.2)
    startButton.shape('start button.gif')

    gameon = True

# handle key press
def handleKeyPress(key):
    global targetLineup

    # find alien with the letter typed and add it to the target line
    if typingMode:
        for alien in aliens:
            if alien.isvisible() and alien.letter == key and alien not in targetLineup:
                targetLineup.append(alien)
                alien.letterGuessed = True

                break

# main game logic
def typingGameLoop(currentId):
    global loopId, currentLoop, targetLineup, currentTarget, movingToTarget, firingLaser, score, letters, playerSpeed, alienSpeed, rampUpMode, modifier, gameon
    
    # prevent game from slowing down when not in typing mode
    if currentLoop != 'typing' or currentId != loopId:
        return

    wn.tracer(False)
    # move aliens
    for alien in aliens:
        if alien.isvisible():
            alien.clear()
            # move aliens and show the letters
            if not(alien.letterGuessed):
                alien.goto(alien.xcor(), alien.ycor() - alienSpeed + 30)
                alien.write(alien.letter, font = ["Minecraft", 32, "normal"], align = "center")
                alien.goto(alien.xcor(), alien.ycor() - 30)

            # move aliens without showing the aliens
            else:
                alien.goto(alien.xcor(), alien.ycor() - alienSpeed)

            # game ends if goes past dotted line
            if alien.ycor() <= -280:
                wn.tracer(True)
                gameon = False
                showEndScreen()
                return
        else:
            # spawn new alien
            randomXValue = random.randint(-270, 250)

            # prevent aliens from overlapping
            repeat = True
            while repeat:
                counter = 0
                # check distance between the respawing alien and the other aliens
                for alien2 in aliens:
                    if ((randomXValue - alien2.xcor())**2 + (300 - alien2.ycor())**2)**(1/2) > 80:
                        counter += 1
                
                # if close to another alien, respawn in a different location
                if counter == len(aliens):
                    repeat = False
                else:
                    randomXValue = random.randint(-270, 250)

            # initialize respawened alien
            alien.goto(randomXValue, 300)
            alien.st()
            alien.color(random.choice(colors))
            alien.shape(random.choice(alienGraphics))
            alien.letter = random.choice(letters)
            alien.letterGuessed = False
            letters.remove(alien.letter)

            # allow for infinite gameplay
            if len(letters) == 0:
                letters = list("abcdefghijklmnopqrstuvwxyz")
            
    wn.tracer(True)

    # set current target to the first item in target lineup
    if not movingToTarget and targetLineup:
        currentTarget = targetLineup.pop(0)
        movingToTarget = True

    # move player to current target
    if movingToTarget and currentTarget:
        wn.tracer(False)
        if abs(player.xcor() - currentTarget.xcor()) > 15:
            if player.xcor() < currentTarget.xcor():
                player.goto(player.xcor() + playerSpeed, player.ycor())
            else:
                player.goto(player.xcor() - playerSpeed, player.ycor())
        else:
            # when player reaches target
            movingToTarget = False
            firingLaser = True
            # shoot laser
            laserSFX.play()
            for laser in lasers:
                # move laser to the start position and bind it to corresponding alien
                if not laser.isvisible():
                    laser.goto(player.xcor(), player.ycor())
                    laser.st()
                    laserAlienMap.append((laser, currentTarget))
                    break
        wn.tracer(True)

    # move laser and detect collision
    for laser, alien in laserAlienMap[:]:
        wn.tracer(False)
        if laser.isvisible():
            # laser movement
            if laser.ycor() < alien.ycor() - 50:
                wn.tracer(False)
                laser.goto(laser.xcor(), laser.ycor() + laserSpeed)
                wn.tracer(True)
            else:
                # laser collision
                alien.ht()
                laser.ht()
                laser.goto(0, -400)
                laserAlienMap.remove((laser, alien))
                explosionSFX.play()

                #increase speed of the alien and player if ramp up mode is on
                if rampUpMode:
                    alienSpeed += .15 * modifier
                    modifier = modifier * .97
                    
                    if playerSpeed < 15:
                        if alienSpeed >= 4 and playerSpeed >= 8:
                            playerSpeed += 0.2
                        else:
                            playerSpeed += 0.3

                # add to score and update score on screen
                score += 1
                scoreTurt.color(random.choice(colors))
                scoreTurt.clear()
                scoreTurt.write(f"Score: {score}", font=['Minecraft', 30, 'normal'], align='center')
        wn.tracer(True)
    
    # continue the gamelogic
    wn.ontimer(lambda: typingGameLoop(currentId), 7)

# function to reset the game
def reset(x, y):
    global restart

    clickSFX.play()

    restartButton.shape('exit button pressed.gif')
    time.sleep(0.1)
    restartButton.shape('exit button.gif')

    restart = True

# show the end screen menu
def showEndScreen():    
    global restart, currentLoop

    currentLoop = None
    
    typingbackgroundSFX.stop()
    arrowbackgroundSFX.stop()

    restart = False

    #hide and show appropriate aliens
    for alien in aliens:
        alien.ht()
        alien.clear()

    for laser in lasers:
        laser.ht()
    
    menuPlayer.goto(player.xcor(), player.ycor())
    menuPlayer.st()
    player.ht()

    scoreTurt.clear()
    dottedLine.clear()
    writeTurt.clear()

    loseSFX.play()

    # stop code for effect
    time.sleep(1)

    menuSound.play(-1)

    # show ship moving to animation position
    while(abs(menuPlayer.xcor()) > 10):
        if menuPlayer.xcor() > 0:
            menuPlayer.goto(menuPlayer.xcor() - 5, -350)
        else:
            menuPlayer.goto(menuPlayer.xcor() + 5, -350)
    menuPlayer.goto(0, -350)

    while (abs(menuPlayer.ycor() - -200) > 10):
        menuPlayer.goto(0, menuPlayer.ycor() + 5)
    menuPlayer.goto(0, -200)

    movingLeft = True

    # move the score writing turtles
    scoreTurt.goto(0,270)
    writeTurt.goto(0, 200)
    scoreTurt.clear()
    scoreTurt.color(random.choice(colors))
    scoreTurt.write("OH NO! An Alien Fell Too Far!", font = ['Minecraft', 50, 'normal'], align = 'center')

    writeTurt.clear()
    writeTurt.color(random.choice(colors))
    writeTurt.write(f"You Destroyed {score} Aliens!!!", font = ["Minecraft", 50, "normal"], align = 'center')
    
    menuAlien1.st()

    # show restart button
    restartButton.st()
    restartButton.goto(0, 0)

    # animation (same as start menu)
    while not(restart):
        if movingLeft:
            if (menuPlayer.xcor() - -200) < -10:
                menuAlien2.shape(random.choice(alienGraphics))
                menuAlien2.st()
                laserSFX.play()
                menuLaser.goto(menuPlayer.xcor(), menuPlayer.ycor())
                menuLaser.st()
                while(menuLaser.ycor() < 125):
                    menuLaser.goto(menuLaser.xcor(), menuLaser.ycor() + 15)
                
                explosionSFX.play()
                movingLeft = False
                menuLaser.ht()
                menuAlien1.ht()
                scoreTurt.clear()
                scoreTurt.color(random.choice(colors))
                scoreTurt.write("OH NO! An Alien Fell Too Far!", font = ['Minecraft', 50, 'normal'], align = 'center')

                writeTurt.clear()
                writeTurt.color(random.choice(colors))
                writeTurt.write(f"You Destroyed {score} Aliens!!!", font = ["Minecraft", 50, "normal"], align = 'center')
                continue

            menuPlayer.goto(menuPlayer.xcor() - 5, menuPlayer.ycor())
        else:
            if (menuPlayer.xcor() - 200) > 10:
                menuAlien1.shape(random.choice(alienGraphics))
                menuAlien1.st()
                movingLeft = True
                laserSFX.play()
                menuLaser.goto(menuPlayer.xcor(), menuPlayer.ycor())
                menuLaser.st()
                while(menuLaser.ycor() < 125):
                    menuLaser.goto(menuLaser.xcor(), menuLaser.ycor() + 15)
                
                menuLaser.ht()
                menuAlien2.ht()
                explosionSFX.play()

                # write score and change score text color for cool effect
                scoreTurt.clear()
                scoreTurt.color(random.choice(colors))
                scoreTurt.write("OH NO! An Alien Fell Too Far!", font = ['Minecraft', 50, 'normal'], align = 'center')

                writeTurt.clear
                writeTurt.color(random.choice(colors))
                writeTurt.write(f"You Destroyed {score} Aliens!!!", font = ["Minecraft", 50, "normal"], align = 'center')
                continue

            menuPlayer.goto(menuPlayer.xcor() + 5, menuPlayer.ycor())
            
    # go back to the menu screen
    showMenu()

# main logic in arrow game mode
def arrowGameLoop(currentId):
    global loopId, currentLoop, targetLineup, currentTarget, movingToTarget, firingLaser, score, letters, playerSpeed, alienSpeed, rampUpMode, modifier, totalAmmo, colors, gameon
    
    # prevent game from slowing down when not in arrow player mode
    if currentLoop != 'arrow' or currentId != loopId:
        return

    wn.tracer(False)
    # move aliens
    for alien in aliens:
        if alien.isvisible():
            alien.clear()
            alien.goto(alien.xcor(), alien.ycor() - alienSpeed)

            # game ends if goes past dotted line
            if alien.ycor() <= -280:
                wn.tracer(True)
                gameon = False
                showEndScreen()
                return
        else:
            # spawn new alien
            randomXValue = random.randint(-270, 250)

            # prevent aliens from overlapping
            repeat = True
            while repeat:
                counter = 0
                # check distance between the respawing alien and the other aliens
                for alien2 in aliens:
                    if ((randomXValue - alien2.xcor())**2 + (300 - alien2.ycor())**2)**(1/2) > 80:
                        counter += 1
                
                # if close to another alien, respawn in a different location
                if counter == len(aliens):
                    repeat = False
                else:
                    randomXValue = random.randint(-270, 250)

            # initialize respawened alien
            alien.goto(randomXValue, 300)
            alien.st()
            alien.color(random.choice(colors))
            alien.shape(random.choice(alienGraphics))
            
    wn.tracer(True)

    # fire laser and detect collision with alien
    for laser in lasers:
        wn.tracer(False)

        laser.st()

        # move the laser up
        laser.goto(laser.xcor(), laser.ycor() + laserSpeed)

        # calculate distances between the laser and aliens
        for alien in aliens:
            # laser collided with alien
            if ((laser.xcor()-alien.xcor())**2 + (laser.ycor()-alien.ycor())**2)**(1/2) < 50:
                explosionSFX.play()

                # hide laser and remove from the list of lasers
                laser.ht()
                lasers.remove(laser)

                # hide the shot alien
                alien.ht()

                # add to score and update score on screen
                score += 1
                scoreTurt.color(random.choice(colors))
                scoreTurt.clear()
                scoreTurt.write(f"Score: {score}", font=['Minecraft', 30, 'normal'], align='center')

                # spawn new alien
                randomXValue = random.randint(-270, 250)

                # prevent aliens from overlapping
                repeat = True
                while repeat:
                    counter = 0
                    # check distance between the respawing alien and the other aliens
                    for alien2 in aliens:
                        if ((randomXValue - alien2.xcor())**2 + (300 - alien2.ycor())**2)**(1/2) > 80:
                            counter += 1
                    
                        # if close to another alien, respawn in a different location
                        if counter == len(aliens):
                            repeat = False
                        else:
                            randomXValue = random.randint(-270, 250)

                # initialize respawened alien
                alien.goto(randomXValue, 300)
                alien.st()
                alien.color(random.choice(colors))
                alien.shape(random.choice(alienGraphics))

                # add 2 bullets to the total ammo
                if random.randint(1, 10) == 1 and totalAmmo < 2:
                    totalAmmo += 2
                else:
                    totalAmmo += 1

                # display ammo update
                writeTurt.clear()
                writeTurt.color(random.choice(colors))
                writeTurt.write(f'Total Bullets: {totalAmmo}', font=['Minecraft', 30, 'normal'], align='center')

                #increase speed of the alien and player if ramp up mode is on
                if rampUpMode:
                    alienSpeed += .15 * modifier
                    modifier = modifier * .97
                    
                    if playerSpeed < 15:
                        if alienSpeed >= 4 and playerSpeed >= 8:
                            playerSpeed += 0.2
                        else:
                            playerSpeed += 0.3

                break
        
        # hide the laser if the laser travled high enough without hitting any aliens
        if laser.ycor() > 350:
            laser.ht()
            lasers.remove(laser)
        
        wn.tracer(True)
    
    # continue the gamelogic
    wn.ontimer(lambda: arrowGameLoop(currentId), 5)

# starting the game
def gameStart():
    global currentLoop, loopId, laserAlienMap, leftPressed, gameMode, difficulty, rightPressed, easyMode, mediumMode, hardMode, targetLineup, movingToTarget, firingLaser, currentTarget, alienSpeed, playerSpeed, laserSpeed, rampUpMode, modifier, gameon, arrowPlayerMode, totalAmmo, lasers, playerShootCooldown

    loopId +=1
    currentId = loopId

    startSFX.play()

    gameon = False

    # Reset movement keys to prevent stuck movement/speed
    leftPressed = False
    rightPressed = False

    wn.tracer(False)
    # initialize turtles
    menuAlien1.ht()
    menuAlien2.ht()
    menuLaser.ht()
    startTurt.ht()
    startTurt.clear()
    startButton.ht()
    arrowModeButton.ht()
    typingModeButton.ht()
    rampUpModeButton.ht()
    easyButton.ht()
    mediumButton.ht()
    hardButton.ht()
    wn.tracer(True)

    # reset variables
    laserAlienMap = []
    targetLineup = []
    movingToTarget = False
    firingLaser = False
    currentTarget = None
    modifier = 1
    playerShootCooldown = 0
    totalAmmo = 6

    if rampUpMode:
        alienSpeed = 1
        playerSpeed = 2
    elif easyMode and arrowPlayerMode:
        alienSpeed = 1
        playerSpeed = 3
    elif mediumMode and arrowPlayerMode:
        alienSpeed = 1.4
        playerSpeed = 4
    elif hardMode and arrowPlayerMode:
        alienSpeed = 1.8
        playerSpeed = 5
    elif easyMode and typingMode:
        alienSpeed = 1
        playerSpeed = 5
    elif mediumMode and typingMode:
        alienSpeed = 2
        playerSpeed = 5
    elif hardMode and typingMode:
        alienSpeed = 3
        playerSpeed = 7


    laserSpeed = 15
   
    writeTurt.goto(0, 300)
    writeTurt.color(random.choice(colors))
    writeTurt.write(f'Game mode: {gameMode}', font = ('Minecraft', 35, 'normal'), align = 'center')
    writeTurt.goto(0, 250)
    writeTurt.color(random.choice(colors))
    writeTurt.write(f'Difficulty: {difficulty}', font = ('Minecraft', 35, 'normal'), align = 'center')
    
    writeTurt.goto(0, 200)
    writeTurt.color(random.choice(colors))
    if arrowPlayerMode:
        writeTurt.write('Use arrow keys to move space to shoot!', font = ('Minecraft', 30, 'normal'), align = 'center')
    else:
        writeTurt.write('Type the letters to kill the aliens!', font = ('Minecraft', 30, 'normal'), align = 'center')    

    

   # animation to show the player go from animation position to start position
    while(abs(menuPlayer.xcor()) > 10):
        if menuPlayer.xcor() > 0:
            menuPlayer.goto(menuPlayer.xcor() - 5, -200)
        else:
            menuPlayer.goto(menuPlayer.xcor() + 5, -200)
    menuPlayer.goto(0, -200)

    while (menuPlayer.ycor() != -350):
        menuPlayer.goto(0, menuPlayer.ycor() - 5)

    player.goto(0, -350)

    menuPlayer.ht()
    player.st()

    # dotted ground line
    dottedLine.up()
    dottedLine.ht()
    dottedLine.color('red')
    dottedLine.speed(0)
    dottedLine.setheading(0)
    dottedLine.goto(-680,-280)


    for i in range(34):
        dottedLine.down()
        dottedLine.fd(20)
        dottedLine.up()
        dottedLine.fd(20)

    #show total ammo if in arrow player mode
    writeTurt.goto(300, 300)

    #show score turtle
    scoreTurt.goto(-300, 300)
    scoreTurt.color(random.choice(colors))
    scoreTurt.write(f"Score: {score}", font=['Minecraft', 30, 'normal'], align='center')

    if arrowPlayerMode:
        lasers.clear()
        lasers = []

    wn.tracer(False)
    if typingMode:
        for i in range(4):
            # laser turtle
            laser = trtl.Turtle()
            laser.up()
            laser.speed(0)
            laser.ht()
            laser.shape('laser.gif')
            lasers.append(laser)
    wn.tracer(True)

    gameon = True

    writeTurt.clear()

    # begin game logic
    if arrowPlayerMode:
        writeTurt.clear()
        writeTurt.color(random.choice(colors))
        writeTurt.write(f'Total Bullets: {totalAmmo}', font=['Minecraft', 30, 'normal'], align='center')
        arrowbackgroundSFX.play(-1)
        currentLoop = 'arrow'
        updateShootCooldown()
        arrowGameLoop(currentId)
    elif typingMode:
        typingbackgroundSFX.play(-1)
        currentLoop = 'typing'
        typingGameLoop(currentId)

# move the player left when left arrow is clicked
def moveLeft():
    global arrowPlayerMode

    wn.tracer(False)
    # move the player
    if leftPressed and arrowPlayerMode and gameon:
        player.goto(player.xcor() - playerSpeed, player.ycor())
    wn.tracer(True)

    # continue to update player position every 5 milliseconds
    wn.ontimer(moveLeft, 5)

# move the player right when right arrow is clicked
def moveRight():
    global arrowPlayerMode

    wn.tracer(False)
    # move the player
    if rightPressed and arrowPlayerMode and gameon:
        player.goto(player.xcor() + playerSpeed, player.ycor())
    wn.tracer(True)

    # continue to update player position every 5 milliseconds
    wn.ontimer(moveRight, 5)

# register that space is clicked to fire a laser
def shootLaser():
    global arrowPlayerMode, lasers, playerShootCooldown, totalAmmo

    wn.tracer(False)

    # shoot when in the correct gamemode, has ammo, if the shoot cooldown is done and if there is active game play
    if arrowPlayerMode and playerShootCooldown > 30 and totalAmmo > 0 and gameon:
        # reset cooldown
        playerShootCooldown = 0

        # create a laser turtle and add it to the list of lasers
        tempTurt = trtl.Turtle(shape = 'laser.gif')
        tempTurt.up()
        tempTurt.speed(0)
        tempTurt.ht()
        tempTurt.goto(player.xcor(), player.ycor())
        lasers.append(tempTurt)
        
        # remove a bullet from total ammo
        totalAmmo -= 1
        writeTurt.clear()
        writeTurt.color(random.choice(colors))
        writeTurt.write(f'Total Bullets: {totalAmmo}', font=['Minecraft', 30, 'normal'], align='center')

        laserSFX.play()

    wn.tracer(True)

# detect key down    
def leftPress():
    global leftPressed
    leftPressed = True

# detect key up
def leftRelease():
    global leftPressed
    leftPressed = False

# detect key down
def rightPress():
    global rightPressed
    rightPressed = True

# detect key up
def rightRelease():
    global rightPressed
    rightPressed = False

# laser shoot cooldown
def updateShootCooldown():
    global playerShootCooldown
    
    playerShootCooldown += 1

    #increase the cooldown value every 2 milliseconds
    if gameon:
        wn.ontimer(updateShootCooldown, 2)

# toogle easy mode
def easyToggle(x,y, clicked):
    global easyMode, difficulty

    # change the shape of the easy mode button and set the easy mode variable
    if easyButton.shape() == 'easy button.gif':
        easyButton.shape('easy button pressed.gif')
        easyMode = True
    else:
        easyButton.shape('easy button.gif')
        easyMode = False

    if clicked:   
        clickSFX.play()

        # if easy mode is toggled, then turn off medium and hard mode
        if mediumMode:
            mediumToggle(None, None, False)

        if hardMode:
            hardToggle(None, None, False)
    
    # show start button if a gamemode is selected
    wn.tracer(False)
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the difficulty
    difficulty = 'Easy'

# toggle medium  mode
def mediumToggle(x,y, clicked):
    global mediumMode, difficulty

    # change the shape of the medium mode button and set the medium mode variable
    if mediumButton.shape() == 'medium button.gif':
        mediumButton.shape('medium button pressed.gif')
        mediumMode = True
    else:
        mediumButton.shape('medium button.gif')
        mediumMode = False

    if clicked:
        clickSFX.play()

        # if medium mode is toggled, then turn off easy and hard mode
        if easyMode:
            easyToggle(None, None, False)

        if hardMode:
            hardToggle(None, None, False)
    
    # show start button if a gamemode is selected
    wn.tracer(False)
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the difficulty
    difficulty = 'Medium'

# toggle hard mode
def hardToggle(x,y, clicked):
    global hardMode, difficulty

    # change the shape of the hard mode button and set the hard mode variable
    if hardButton.shape() == 'hard button.gif':
        hardButton.shape('hard button pressed.gif')
        hardMode = True
    else:
        hardButton.shape('hard button.gif')
        hardMode = False

    if clicked:
        clickSFX.play()

        # if hard mode is toggled, then turn off easy and medium mode
        if easyMode:
            easyToggle (None, None, False)
        
        if mediumMode:
            mediumToggle(None, None, False)
    
    # show start button if a gamemode is selected
    wn.tracer(False)
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the difficulty
    difficulty = 'Hard'

# toggle arrow mode
def arrowToggle(x,y, clicked):
    global arrowPlayerMode, gameMode

    # change the shape of the arrow mode button and set the arrow player mode variable
    if arrowModeButton.shape() == 'arrow mode button.gif':
        arrowModeButton.shape('arrow mode button pressed.gif')
        arrowPlayerMode = True
    else:
        arrowModeButton.shape('arrow mode button.gif')
        arrowPlayerMode = False
    
    if clicked:  
        clickSFX.play()

        # if arrow player mode is toggled, then turn off typing mode
        if typingMode:
            typingToggle(None, None, False)

    # show start button if a gamemode is selected
    wn.tracer(False)
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the game mode
    gameMode = 'Arrow Key'

# toggle typing mode
def typingToggle(x, y, clicked):
    global typingMode, gameMode

    # change the shape of the typing mode button and set the typing mode variable
    if typingModeButton.shape() == 'typing mode button.gif':
        typingModeButton.shape('typing mode button pressed.gif')
        typingMode = True
    else:
        typingModeButton.shape('typing mode button.gif')
        typingMode = False
 
    if clicked:
        clickSFX.play()

        # if typing mode is toggled, then turn off arrow player mode
        if arrowPlayerMode:
            arrowToggle(None, None, False)

    # show start button if a gamemode is selected
    wn.tracer(False)
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the game mode
    gameMode = 'Typing'

# toggle ramp up mode
def rampUpToggle(x, y):
    global rampUpMode, difficulty

    clickSFX.play()

    # hide difficulty buttons
    if rampUpModeButton.shape() == 'ramp up mode button.gif':
        rampUpModeButton.shape('ramp up mode button pressed.gif')
        rampUpMode = True

        wn.tracer(False)
        easyButton.ht()
        mediumButton.ht()
        hardButton.ht()
        wn.tracer(True)
    # show difficulty buttons
    else:
        rampUpModeButton.shape('ramp up mode button.gif')
        rampUpMode = False
        
        wn.tracer(False)
        easyButton.st()
        mediumButton.st()
        hardButton.st()
        wn.tracer(True)

    # show start button if a gamemode is selected
    wn.tracer(False)
    # hide start button if no gamemode is selected
    if ((easyMode or mediumMode or hardMode) and (arrowPlayerMode or typingMode)) or (rampUpMode and (arrowPlayerMode or typingMode)):
        startButton.st()
    else:
        startButton.ht()
    wn.tracer(True)

    # set the difficulty
    difficulty = 'Ramp Up'


#--------------------------------MAIN--------------------------------


initTurtles()

# key bindings
for letter in list("abcdefghijklmnopqrstuvwxyz"):
    wn.onkeypress(lambda let=letter: handleKeyPress(let), letter)

# onclick detection
startButton.onclick(whenClicked)
restartButton.onclick(reset)

# menu buttons onclick detection
easyButton.onclick(lambda x, y: easyToggle(x, y, True))
mediumButton.onclick(lambda x, y: mediumToggle(x, y, True))
hardButton.onclick(lambda x, y: hardToggle(x, y, True))
arrowModeButton.onclick(lambda x, y: arrowToggle(x, y, True))
typingModeButton.onclick(lambda x, y: typingToggle(x, y, True))
rampUpModeButton.onclick(rampUpToggle)


# show the menu on program start
menuSound.play(-1)
showMenu()

# detect left movement
wn.onkeypress(leftPress, "Left")
wn.onkeyrelease(leftRelease, "Left")


# detect right movement
wn.onkeypress(rightPress, "Right")
wn.onkeyrelease(rightRelease, "Right")

# detect if player wants to shoot a laser
wn.onkeyrelease(shootLaser, 'space')

# begin player movement
moveRight()
moveLeft()

wn.listen()
wn.mainloop()