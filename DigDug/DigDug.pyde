# Created by Ryan B. Green in May/June 2019
import pickle

add_library('minim')

def mergeSort(nums):
    """ Sorts a list of numbers """

    if len(nums) < 2: # checks if too small to split
        return

    left = nums[: len(nums) // 2] # splits into two lists
    right = nums[len(nums) // 2:]

    mergeSort(left) # splits left list (and sorts if size is larger than 1)

    mergeSort(right) # splits right list (and sorts if size is larger than 1)

    ri = 0
    li = 0
    count = 0

    while (ri < len(right)) or (li < len(left)): # merges two lists together (sorted)

        while ((ri >= len(right)) and (li < len(left))) or ((li < len(left)) and (left[li] <= right[ri])): # left list
            nums[count] = left[li]
            li += 1 # shifts left marker over
            count += 1

        while ((li >= len(left)) and (ri < len(right))) or ((ri < len(right)) and (right[ri] <= left[li])): # right list
            nums[count] = right[ri]
            ri += 1 # shifts right marker over
            count += 1

class Miner():
    """ Stores all of the methods and attributes related to the player """
    
    def __init__(self, model, shield, minim):
        """ Initializes the attributes of the player """
        self.model = model #stores the spritesheet
        self.x = 315 # player's x-coordinate
        self.y = 405 # player's y-coordinate
        self.modeX = 0 # element of spritesheet x-coordinate
        self.modeY = 0 # element of spritesheet y-coordinate
        self.gridX = 7 # x-coordinate of square player is in
        self.gridY = 6 # y-coordinate of square player is in
        self.score = 0 # player's score
        self.weapon = False # if weapon is active currently
        self.direction = 0 # which direction the player is facing (0->right, 90->down, 180->left, 270->up)
        self.timeSinceAttack = 0 # time weapon was fired
        self.animationFrameTime = 0 # last time walk animation frame changed
        self.animationToggle = 0 # stores which frame the animation is on
        self.pumpCount = 0 # must pump 5 times to kill enemy (stores # of pumps)
        self.killEnabled = False # stores whether 5 pumps have occured 
        self.shield = shield # stores image of shield
        self.shieldTimer = 0 # stores time since start of stage
        self.shieldEnabled = True #stores whether the spawn shield is active or not
        self.lives = 5 # stores number of lives remaining (dies when reaches 0)
        self.name = "" # stores player's username (can't be one on highscore list)
        self.playedSince = False #stores whether the player has played since the highscore list has been opened
        self.lastMoved = 0 # stores the time since the player started moving
        self.deathSound = minim.loadFile("digDugDie.mp3") # stores the sound that plays when the player dies
        
        
    
    def render(self):
        """ Draws Dig Dug onto the screen """
        
        pushMatrix()
        translate(self.x, self.y) # translates to the player's coordiantes to allow for transformations
            
        if self.direction == 90: # facing downwards
            rotate(radians(self.direction)) 
            
            if self.weapon: # draws weapon (if enabled)
                image(self.model, 0, -30, 96, 15, 96, 168, 192, 183) 
                
            # draws Dig Dug according to current variant and animation cycle
            image(self.model, -45 * cos(radians(self.direction)), -45 * sin(radians(self.direction)), 39, 46, 0 + (49 * self.modeX) + self.animationToggle, 0 + (48 * self.modeY), 48 + (49 * self.modeX) + self.animationToggle, 45 + (48 * self.modeY))
        
        elif self.direction == 180: # move left
             scale(-1,1)
             
             if self.weapon: # draws weapon (if enabled)
                image(self.model, -15, 25, 96, 15, 96, 168, 192, 183) 
             
             # draws Dig Dug according to current variant and animation cycle
             image(self.model, -45, 0, 39, 46, 0 + (49 * self.modeX) + self.animationToggle, 0 + (48 * self.modeY), 48 + (49 * self.modeX) + self.animationToggle, 45 + (48 * self.modeY))
        
        elif self.direction == 270: # move up
             rotate(radians(self.direction))
             
             if self.weapon: # draws weapon (if enabled)
                image(self.model, -25, 15, 96, 15, 96, 168, 192, 183) 
            
             # draws Dig Dug according to current variant and animation cycle
             image(self.model, 45 * sin(radians(self.direction)), 45 * cos(radians(self.direction)), 39, 46, 0 + (49 * self.modeX) + self.animationToggle, 0 + (48 * self.modeY), 48 + (49 * self.modeX) + self.animationToggle, 45 + (48 * self.modeY))
        
        elif self.direction == 0: # move right
             
             if self.weapon: # draws weapon (if enabled)
                image(self.model, 15, 15, 96, 15, 96, 168, 192, 183) 
            
             # draws Dig Dug according to current variant and animation cycle
             image(self.model, 0, 0, 39, 46, 0 + (49 * self.modeX) + self.animationToggle, 0 + (48 * self.modeY), 48 + (49 * self.modeX) + self.animationToggle, 45 + (48 * self.modeY))
        
        popMatrix()
        
        if self.shieldEnabled: # protective shield for first 5 seconds of each round (enemies can't move, just player)
            image(self.shield, self.x - 10, self.y - 10, self.shield.width // 8, self.shield.height // 8) # draws shield on player's location
            
            if millis() - self.shieldTimer >= 5000: # disables shield 5 seconds after round start
                self.shieldEnabled = False
        
        
        for n in range(1, self.lives + 1): # draws lives on the top-right of the screen
            image(self.model, 675 - (45 * n), 0, 39, 46, 0 + (49 * self.modeX), 0 + (48 * self.modeY), 48 + (49 * self.modeX), 45 + (48 * self.modeY))
        
        
        
    def move(self, dir, dug):
        """ Moves Dig Dug """
        
        if not(self.weapon) and not(self.killEnabled): # moves player (when not firing weapon)
            
            if millis() - self.animationFrameTime >= 750: # toggles between 2 frames of walking animation
                if self.animationToggle == 0:
                    self.animationToggle = 49
                else:
                    self.animationToggle = 0
            
            if (dir == 'a') and (self.x >= 5): # left movement (when not at left edge)
                
                self.direction = 180 # adjusts direction of movement
                
                if (self.y % 45) == 0: # checks if centered (vertically) to move
                    
                    self.x -= 5 # adjusts x-coordinate
                    
                    if (self.gridX * 45) > self.x: # checks if player has moved into left square
                        self.gridX -= 1 # adjusts x-coordinate of grid
                        if dug[self.gridY][self.gridX] == 0:
                            dug[self.gridY][self.gridX] = 'l' # digs left square
                            
                            self.score += 10 # adds points for digging
            
            elif (dir == 'd') and (self.x <= 630): # right movement (when not at right edge)
                
                self.direction = 0 # adjusts direction of movement
                
                if (self.y % 45) == 0: # checks if centered (vertically) to move
                    
                    self.x += 5 # adjusts x-coordinate
                    
                    if ((self.gridX * 45) + 44) < self.x: # checks if player has moved into right square
                        self.gridX += 1 # adjusts x-coordinate of grid
                        if dug[self.gridY][self.gridX] == 0:
                            dug[self.gridY][self.gridX] = 'r' # digs right square
                            
                            self.score += 10 # adds points for digging
            
            elif (dir == 's') and (self.y <= 760): # down movement (when not at bottom edge)
                
                self.direction = 90 # adjusts direction of movement
                
                if (self.x % 45) == 0: # checks if centered (horizontally) to move
                    
                    self.y += 5 # adjusts y-coordinate
                    
                    if ((self.gridY * 45) + 44) < (self.y - 135): # checks if player has moved into below square
                        self.gridY += 1 # adjusts y-coordinate of grid
                        
                        if dug[self.gridY][self.gridX] == 0:
                            dug[self.gridY][self.gridX] = 'd' # digs below square
                            
                            self.score += 10 # adds points for digging
                
            elif (dir == 'w') and (self.y >= 140): # up movement (when not at top edge)
                
                self.direction = 270 # adjusts direction of movement
                
                if (self.x % 45) == 0:# checks if centered (horizontally) to move
                    
                    self.y -= 5 # adjusts y-coordinate
                    
                    if (self.gridY * 45) > (self.y - 135): # checks if player has moved into above square
                        self.gridY -= 1 # adjusts y-coordinate of grid
                        
                        if dug[self.gridY][self.gridX] == 0:
                            dug[self.gridY][self.gridX] = 'u' # digs above square
                            
                            self.score += 10 # adds points for digging

    
    
    def attack(self, time = None):
        """ Activates player's attack and counts pumps while attacking """
        
        if not(self.weapon): # activates weapon
            self.timeSinceAttack = time
            self.weapon = True
            self.pumpCount = 0
        
        else: # increments # of pumps
            self.pumpCount += 1
            
            if self.pumpCount >= 5: # checks if 5 pumps
                self.killEnabled = True # activates killing
             
            
    def retract(self):
        """ Checks if it is time to retract weapon and retracts it if so """
        
        if millis() - self.timeSinceAttack >= 1000:
            self.weapon = False
            self.killEnabled = False
    
    
    def checkHit(self, badGuy):
        """ Checks collisions between the player and enemies """
        
        if (badGuy.gridX == self.gridX) and (badGuy.gridY == self.gridY): # if in same grid-coordinates as enemy
            player.x, player.y, player.gridX, player.gridY, player.direction, player.shieldEnabled, player.shieldTimer = (315, 405, 7, 6, 0, True, millis()) # reset to middle & activate shield
            player.lives -= 1 # subtract a life
            self.deathSound.play() # plays Dig Dug's death sound
            self.deathSound.rewind() # rewinds Dig Dug's death sound
            
            
                    

        
class Pest():
    """ Stores the methods and attributes belonging to an enemy """
    def __init__(self, type, x, y, gridx, gridy, model, ghostSound, death, escape):
        """ Initializes the attributes of the enemy """
        self.model = model # stores spritesheet
        self.x = x # stores x-coordinate of enemy
        self.y = y # stores y-coordinate of enemy
        self.variantX = 0 # stores x-coordinate in spritesheet of enemy
        self.variantY = 9 # stores y-coordinate in spritesheet of enemy
        self.gridX = gridx # stores x-coordinate in grid of enemy
        self.gridY = gridy # stores y-coordinate in grid of enemy
        self.direction = 0 # stores direction enemy is facing (0 -> right, 1 -> down, 2 -> left, 3 -> right)
        self.stuck = False # stores whether the enemy is stuck in player's weapon (True -> is stuck, False -> isn't stuck)
        self.ghost = False # stores whether the enemy's ghost mode is active
        self.ghostGoal = [0, 0] # x, y grid of dig dug when becomes ghost
        self.which = int(random(-0.49, 1.49)) # stores which type of enemy it is (dragon or orange thing)
        self.sounds = {"ghost" : ghostSound, "die" : death, "escape": escape} # stores the sounds that are related to the enemies

    
    def render(self):
        """ Draws the enemy onto the screen """
        # draws the enemy according to location and type
        image(self.model, self.x, self.y, 39, 42, 0 + (49 * self.variantX), 0 + (48 * (self.variantY + (self.which * 6))), 45 + (49 * self.variantX), 45 + (48 * (self.variantY + (self.which * 6))))
    
   
    def move(self, dug, numAllies, digDugGridX, digDugGridY, justBegan):
        """ Generates Enemy Pathing & Movement """
        
        if not(self.stuck) and not(self.ghost) and not(justBegan): # if stuck in player's weapon, if in ghost mode, or if within beginning period
            self.variantY = 9 # sets model type to default
            
            if (numAllies == 1) and (self.gridY == 0) and ((self.y % 45 == 0)): # checks if last remaining enemy and if on first row (in moveable area)
                self.direction = 2 # sets direction to left
                if (self.x % 45 == 0) and ((self.gridX == 0) or (dug[self.gridY][self.gridX - 1] == 0)): # checks if in top-left
                    self.sounds["escape"].play() # plays the escape sound
                    self.sounds["escape"].rewind()  # rewinds the escape sound
                    return True # returns that the enemy has escaped
                else:
                    self.x -= 2.5 # adjusts enemy's x-coordinate to move left
                    if (self.gridX * 45) > self.x: # adjusts enemy's x-coordinate for grid
                        self.gridX -= 1
                
    
        
            elif self.direction == 0: # moves right
                if (self.x % 45 == 0) and ((self.gridX == 14) or (dug[self.gridY][self.gridX + 1] == 0)): # checks if enemy can't move right (improper y-coord or on right edge)
                    self.direction = int(random(0, 4)) # randomly changes direction
                else:
                    self.x += 2.5 # adjusts enemy's x-coordinate to move right
                    if ((self.gridX * 45) + 44) < self.x: # adjusts enemy's x-coordinate for grid
                        self.gridX += 1
                    
                  
                        
            
            elif self.direction == 2: #left
                if (self.x % 45 == 0) and ((self.gridX == 0) or (dug[self.gridY][self.gridX - 1] == 0)): # checks if enemy can't move left (improper y-coord or on left edge)
                    self.direction = int(random(-0.45, 3.45)) # randomly changes direction
                else:
                    self.x -= 2.5  # adjusts enemy's x-coordinate to move left
                    if (self.gridX * 45) > self.x: # adjusts enemy's x-coordinate for grid
                        self.gridX -= 1
                    
                    self.variantY = 10
                        
            elif self.direction == 1: #down
                if (self.y % 45 == 0) and ((self.gridY == 14) or (dug[self.gridY + 1][self.gridX] == 0)): # checks if enemy can't move down (improper x-coord or on bottom edge)
                    self.direction = int(random(-0.45, 3.45)) # randomly changes direction
                else:
                    self.y += 2.5  # adjusts enemy's x-coordinate to move down
                    if ((self.gridY * 45) + 44) < (self.y - 135): # adjusts enemy's y-coordinate for grid
                        self.gridY += 1
            
            else: # up
                if (self.y % 45 == 0) and ((self.gridY == 0) or (dug[self.gridY - 1][self.gridX] == 0)): # checks if enemy can't move up (improper x-coord or on top edge)
                    self.direction = int(random(-0.45, 3.45)) # randomly changes direction
                else:
                    self.y -= 2.5  # adjusts enemy's x-coordinate to move up
                    if ((self.gridY * 45)) > (self.y - 135): # adjusts enemy's y-coordinate for grid
                        self.gridY -= 1
            
            if (int(random(0, 15)) == 5) and (self.x % 45 == 0) and (self.y % 45 == 0): # random changes direction to reduce predictability
                self.direction = int(random(0, 4))
                
            elif (int(random(0, 125)) == 5) and (self.x % 45 == 0) and (self.y % 45 == 0): # random changes to ghost form reduce predictability
                self.ghost = True
                self.variantY = 9
                self.variantX += 3 + (self.which * 3) # changes to ghost image
                self.ghostGoal = [digDugGridX, digDugGridY] # sets goal destination to player's current location (at time of becoming ghost)
                self.sounds["ghost"].play() # plays the ghost activation sound
                self.sounds["ghost"].rewind()  # rewinds the ghost activation sound

        elif self.ghost and not(self.stuck) and not(justBegan): # ghost movement
            if self.gridX < self.ghostGoal[0]: # if left of goal
                self.x += 2.5 # adjusts enemy's x-coordinate to move right
                if ((self.gridX * 45) + 44) < self.x: # adjusts enemy's x-coordinate for grid
                    self.gridX += 1
           
            elif self.gridX > self.ghostGoal[0]: # if right of goal
                self.x -= 2.5 # adjusts enemy's x-coordinate to move left
                if (self.gridX * 45) > self.x: # adjusts enemy's x-coordinate for grid
                    self.gridX -= 1
            
            if self.gridY < self.ghostGoal[1]: # if above goal
                self.y += 2.5 # adjusts enemy's x-coordinate to move down
                if ((self.gridY * 45) + 44) < (self.y - 135): # adjusts enemy's y-coordinate for grid
                    self.gridY += 1
            
            elif self.gridY > self.ghostGoal[1]: # if below goal
                self.y -= 2.5 # adjusts enemy's x-coordinate to move up
                if ((self.gridY * 45)) > (self.y - 135): # adjusts enemy's y-coordinate for grid
                    self.gridY -= 1
            
            if (self.gridY == self.ghostGoal[1]) and (self.gridX == self.ghostGoal[0]): # disables ghost form if reaches destination
                self.variantX -= 3 + (self.which * 3) # returns back to normal form
                self.ghost = False
                self.x = self.gridX * 45
                self.y = 135 + (self.gridY * 45)            
            
        
            
        
        return False # returns that the enemy hasn't escaped
            
    
            
        
            
        
    
    def checkHit(self, digDug):
        """ Checks if enemy hits player's weapon """
        if ((digDug.direction == 0) and (0 <= abs(self.y - digDug.y) <= 22.5) and (digDug.x <= self.x <= (digDug.x + 111))) or \
              ((digDug.direction == 90) and (0 <= abs(self.x - digDug.x) <= 22.5) and (digDug.y <= self.y <= (digDug.y + 111))) or \
              ((digDug.direction == 180) and (0 <= abs(self.y - digDug.y) <= 22.5) and ((digDug.x - 111) <= self.x <= digDug.x)) or \
              ((digDug.direction == 270) and (0 <= abs(self.x - digDug.x) <= 22.5) and ((digDug.y - 111) <= self.y <= digDug.y)):
            # ^ Checks if within bounds of weapon
            if not(digDug.killEnabled) and not(digDug.weapon): # disables enemy movement if in range
                self.stuck = True # freezes enemy
                self.variantY = 11 + (self.which * 2) # adjusts model of the enemy
                self.variantX = 0
                return False # returns that the enemy hasn't died
            
            elif digDug.killEnabled and self.stuck: # kills enemy if pumped 5 times
                self.sounds["die"].play() # plays enemy death sound
                self.sounds["die"].rewind() # rewinds enemy death sound
                return True # returns that the enemy has died
            
            else:
                return False # doesn't kill enemy if not pumped enough
              
              


class Level():
    """ Stores methods & attributes for stages, high scores, and the main menu """
    
    def __init__(self, spriteSheet, minim):
        """ Initializes the attributes of the levels """
        
        self.spriteSheet = spriteSheet # stores the spritesheet
        self.model = loadImage("mainTitleLogo.png") # stores the game's logo
        self.dug, self.spawnCoords = ("placeholder", "also") # stores the dug areas and the spawn areas respectively
        self.mode = 'menu' # stores the current mode ('menu', 'play', 'scores', or 'gameOver')
        self.enemies = [] # stores the enemies
        self.font = loadFont("ArcadeNormal-48.vlw") # stores the font
        textFont(self.font)
        self.high_scores = [] # stores the current high scores
        self.possibleCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" # stores the possible characters for usernames
        self.name = [0, 0, 0] # stores the currently selected username
        
        file = open( "scores.txt", 'rb' ) # opens and reads in binary the high score file
        self.usedNames = pickle.load( file ) # extracts dictionary of top 5
        file.close() # closes file
        
        self.usedNames = list(self.usedNames.values()) # stores the already used names (in top 5)
        self.invalidName = False # stores if the currently selected name is already being used in the high scores
        
        self.sounds = {"walkMusic" : minim.loadFile("walkMusic.wav"), "shoot" : minim.loadFile("weaponFire.mp3"), "ghost" : minim.loadFile("monsterGhost.mp3"),\
                        "enemyDie" :  minim.loadFile("monsterDie.mp3"), "escape" : minim.loadFile("monsterEscape.mp3"), "start" : minim.loadFile("menuStart.mp3"),\
                          "play" : minim.loadFile("playStart.mp3") } # stores the audio files
        
        self.sounds["walkMusic"].loop() # sets the music to infinitely loop
        self.sounds["walkMusic"].pause() # pauses the music
        
        self.sounds["start"].play() # plays starting jingle
        self.sounds["start"].rewind() # rewinds starting jingle
        
    def render(self):
        if (self.mode == 'play'): # if game is being played
            background(0) # sets black background
            
            fill(135, 185, 185)
            rect(0, 0, 675, 135) # draws sky
            
            for y in range(len(self.dug)): # draws dirt & tunnels
                for x in range(len(self.dug[0])):
                    if self.dug[y][x] == 0: # adjusts dirt colour (darker the lower you go)
                        if y == 0: 
                            fill(108, 7, 0)
                        elif 1 <= y <= 3:
                            fill(255, 184, 0)
                        elif 4 <= y <= 7:
                            fill(222, 104, 0)
                        elif 8 <= y <= 11:
                            fill(184, 33, 0)
                        else:
                            fill(151, 0, 0)

    
                        rect(x * 45, 135 + (y * 45), 45, 45) # draws squares
                    
                    elif self.dug[y][x] == 'l': # draws left-dug tunnel
                        fill(108, 7, 0)
                        rect((x * 45) + 22.5, 135 + (y * 45), 45, 45)
                    
                    elif self.dug[y][x] == 'r': # draws right-dug tunnel
                        fill(108, 7, 0)
                        rect((x * 45) - 22.5, 135 + (y * 45), 45, 45)
                    
                    elif self.dug[y][x] == 'd': # draws downward-dug tunnel
                        fill(108, 7, 0)
                        rect(x * 45, (135 + (y * 45)) - 22.5, 45, 45)
                    
                    elif self.dug[y][x] == 'u': # draws upward-dug tunnel
                        fill(108, 7, 0)
                        rect(x * 45, (135 + (y * 45)) + 22.5, 45, 45)
                    
                    else: # draws fully-dug tunnel (for vertical pre-generated tunnels)
                        fill(108, 7, 0)
                        rect(x * 45, 135 + (y * 45), 45, 45)
                        
                    
                    
        elif self.mode == 'menu': # if on main menu
            
            background(0) # sets background to black
            textMode(CENTER)
            
            textSize(25)
            if ((285 <= mouseX <= 385) and (380 <= mouseY <= 405)) and not(self.invalidName): # if mouse is over play button
                fill(225, 215, 115)
                text("PLAY", 289, 404) # highlights play button
            
            fill(255, 255, 255)  
            text("PLAY", 290, 405) # play button
            
            if (210 <= mouseX <= 455) and (450 <= mouseY <= 475): # if mouse is over highscores button
                fill(225, 215, 115)
                text("HIGHSCORES", 214, 474) # highlights highscores button
            
            fill(255, 255, 255)  
            text("HIGHSCORES", 215, 475) # highscores button
            
            textSize(35)
            
            # highlights up buttons if they are hovered over
            if (547 <= mouseY <= 557):
                if (390 <= mouseX <= 405):
                    fill(225, 215, 115)
                    text("    ^", 244.5, 579.5)
                
                elif (322 <= mouseX <= 336):
                    fill(225, 215, 115)
                    text("  ^  ", 244.5, 579.5) 
                
                elif (252 <= mouseX <= 268):
                    fill(225, 215, 115)
                    text("^    ", 244.5, 579.5) 
                
            fill(255, 255, 255)
            
            text("^ ^ ^", 245, 580) # up bottons
            
            if "".join([self.possibleCharacters[self.name[n]] for n in range(3)]) in self.usedNames: # if name already in highscore list => invalid
                self.invalidName = True
                fill(255, 0, 0)
            else:
                self.invalidName = False
                           
            text(" ".join([self.possibleCharacters[self.name[n]] for n in range(3)]), 245, 600) # draws current name selection
            
            pushMatrix()
            scale(1,-1)
            if (610 <= mouseY <= 620):  # highlights down buttons if they are hovered over
                if (390 <= mouseX <= 405):
                    fill(225, 215, 115)
                    text("    ^", 244.5, -591.5)
                
                elif (322 <= mouseX <= 336):
                    fill(225, 215, 115)
                    text("  ^  ", 244.5, -591.5) 
                
                elif (252 <= mouseX <= 268):
                    fill(225, 215, 115)
                    text("^    ", 244.5, -591.5) 
                    
            fill(255, 255, 255)
            text("^ ^ ^", 245, -592) # down bottons
            popMatrix()
                        
            textSize(15)
            if (0 <= mouseX <= 180) and (790 <= mouseY <= 815):
                fill(225, 215, 115)
                text("INSTRUCTIONS", 1.75, 806.75) # draws title
                
            fill(255, 255, 255)
            text("INSTRUCTIONS", 2.5, 807.5) # draws title
            
            
            imageMode(CENTER)
            image(self.model, 337.5, 175, self.model.width / 2, self.model.height / 2) # draws logo
            imageMode(CORNER)
            textMode(CORNER)
        
        elif self.mode == 'scores': # if on highscore screen
            background(0)
            textSize(50)
            text("HIGHSCORES", 100, 175) # draws title
            textSize(25)
            
            for item in range(len(self.high_scores)): # draws highscores
                self.high_scores[item][1] = str(self.high_scores[item][1])
                text("       ".join(self.high_scores[item]), 170, 400 + (item * 45))
        
        
        elif self.mode == 'instructions': # Displays instructions for the player to read
            background(0)
            textSize(30)
            text("INSTRUCTIONS", 160, 175) # draws title
            textSize(20)
            text("Move Dig Dug using WASD!", 100, 275)
            text("To shoot, click the mouse button!", 17.5, 375)
            textSize(15)
            text("Dig Dug dies via contact with an enemy.", 55, 480)
            textSize(10)
            text("Dig Dug's feet must be laying on a floor/wall to be able to move.", 22.5, 300)
            text("If an enemy is caught by the weapon, click 5 times to kill them.", 27.5, 400)
            text("Dig Dug's weapon only lasts 1 second, so you must act quickly!", 35, 415)


            textSize(8)
            text("The lower down you kill an enemy, the higher the points that you are awarded!", 35, 430)
            text("If there is only one enemy remaining, it can escape in the top-left corner!", 45, 495)
            text("Enemies can pass through walls while in their ghost form, so watch out!", 60, 510)

            

        
        
    def stageLoad(self, specifier):
        """ Changes stage layout """
        
        # Default settings (for every level)
        self.dug = [[0 for n in range(15)] for n in range(15)]
        self.dug[0] = ['l', 'l', 'l', 'l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
        self.dug[6][6:9] = ['l', 'd', 'r']
        tempY = 0
        tempX = 0
        tempLen = 0
        for n in range(1, 6):
            self.dug[n][7] = 'd'
        self.spawnCoords = []
        
        if specifier == 0: # level 1 (same evey time)
            
            # sets pre-dug tunnels
            
            self.dug[3][10:14] = ['l', 'l', 'r', 'r'] 
            
            for n in range(2, 6):
                self.dug[n][1] = 'u'
                self.dug[12][n] = 'l'
                self.dug[8 + n][11] = 'd'
            self.dug[6][1] = 'd'
            self.dug[12][6] = 'r'
            self.dug[10][11] = 'u'
            
            self.spawnCoords = [(3, 12), (1, 3), (12, 3), (11, 11)] # sets spawn coordinates
        
            
        
        elif specifier == 1: # random levels (after level 1)
            
            for n in range(2): # creates max of 4 tunnels (with guaranteed 4 enemies)
                # HORIZONTAL TUNNEL
                tempX = int(random(0, 13))
                tempY = int(random(2, 13))
                
                tempLen = int(random(3, 5))
                
                while 14 < (tempX + tempLen):
                    tempLen -= 1
                    
                self.dug[tempY][tempX : tempX + tempLen] = ['f' for n in range(tempLen)]
                
                self.spawnCoords.append((tempX + 1, tempY))
                
                # VERTICAL TUNNEL
                
                tempX = int(random(0, 13))
                tempY = int(random(2, 13))
                tempLen = int(random(3, 5))
                
                while 14 < (tempY + tempLen):
                    tempLen -= 1
                
                for n in range(tempY, tempY + tempLen):
                    self.dug[n][tempX] = ['f' for w in range(tempLen)]
                
                self.spawnCoords.append((tempX, tempY + 1))
        
        self.enemies = [] # resets enemies
        
        for n in range(len(self.spawnCoords)): # adds enemies to list (at spawnpoints)
            tempX, tempY = self.spawnCoords[n]
            self.enemies.append(Pest(1, tempX * 45, (tempY * 45) + 135, tempX, tempY, spriteSheet, self.sounds["ghost"], self.sounds["enemyDie"], self.sounds["escape"]))
    
    def scoreAllocation(self, digDug):
        """ Sorts scores into top 5 """
        file = open( "scores.txt", 'rb' ) # read from high score file in binary
        scores = pickle.load( file ) 
        file.close()
        
        sortedScores = list(scores.keys()) # creates list of scores
        
        if digDug.playedSince: # adds player's score if hasn't played since last time sorted
            sortedScores += [digDug.score]
            scores[digDug.score] = digDug.name
            
        
        mergeSort(sortedScores) # sorts scores
        self.high_scores = [[scores[sortedScores[n]], sortedScores[n]] for n in range(len(sortedScores) - 1, -1, -1)] # places in high score list
        
        
        if digDug.playedSince: # if player hasn't played since
            if len(scores) > 5: # removes worst score
                del scores[sortedScores[0]]
                del self.high_scores[-1]
            
            with open('scores.txt', 'wb') as f: # writes highscores back to score file in binary
                pickle.dump(scores, f, protocol=2)
            f.close()
            
            digDug.playedSince = False # says sorted since last played 
            self.usedNames = list(scores.values()) # updates used names
             
        
            
 

def setup():
    global player, stage, spriteSheet, minim # sets global variables
    size(15 * 45, 135 + (15 * 45)) # sets size of window
    
    minim = Minim(this)
    spriteSheet = loadImage("spritesTransparent.png") # loads spritesheet
    player = Miner(spriteSheet, loadImage("shield.png"), minim) # sets up player
    stage = Level(spriteSheet, minim) # sets up stages
    stage.stageLoad(0) # initializes 1st stage
    

    
def draw():
    
    stage.render() # draws stage to screen
    
    if stage.mode == 'play': # if in game mode
        player.render() # draws player to screen
         
        adjustor = 0 # adjusts for killed enemies
        
        if stage.enemies == ["done"]: # if no enemies remaining
            stage.stageLoad(1) # generates new random stage
            player.x, player.y, player.gridX, player.gridY, player.direction, player.shieldEnabled, player.shieldTimer, player.playedSince = (315, 405, 7, 6, 0, True, millis(), True) # resets player for new stage
        else:
            for mob in range(len(stage.enemies)): # iterates through all enemies
                if stage.enemies != ["done"]: # if enemies still remaining
                    if stage.enemies[mob + adjustor].move(stage.dug, len(stage.enemies), player.gridX, player.gridY, player.shieldEnabled): # moves enemy; if 1 enemy left, they can escape at top left (0,0)
                        stage.enemies = ["done"] # if no enemies left
                        break
                    else:
                        stage.enemies[mob + adjustor].render() # draws enemies to screen
                    
                    if stage.enemies != ["done"]: # if still enemies remaining
                        if not(player.shieldEnabled): # checks if round has started
                            player.checkHit(stage.enemies[mob + adjustor]) # checks if in range of weapon
                            
                            if player.weapon: # when player's weapon is activated
                                if stage.enemies[mob + adjustor].checkHit(player): # checks if enemy is in range
                                    player.score += 100 * (stage.enemies[mob + adjustor].gridY + 1) # adds score if kills enemy (more if lower down)
                                    if len(stage.enemies) == 1: # if there was only 1 enemy left
                                        stage.enemies = ["done"]
                                    else:
                                        stage.enemies.pop(mob + adjustor) # if there were more than 1 enemy left
                                    
                                    adjustor -= 1 # adjusts for less enemies
                                    
                            else:
                                stage.enemies[mob + adjustor].stuck = False # stops the enemy from being stuck by weapon (when time runs out)
                        
                else:
                    break # breaks if no enemies left
    
        if player.weapon: # retracts weapon after 2 seconds
            player.retract()
    
        textSize(10)
        fill(255, 255, 255)
        text("Score: %s"%(player.score), 10, 15) # draws score to screen
        
        if player.lives <= 0: # ends game if player runs out of lives
            stage.mode = 'gameOver' # changes to game over screen
            stage.enemies = [] # eliminates enemies
            stage.scoreAllocation(player) # allocates player's score to high score list
        
        if (millis() - player.lastMoved) >= (stage.sounds["walkMusic"].length() + 100):
            
            player.lastMoved = 0
                    
        
    elif stage.mode == 'gameOver': # if game is over
        fill(135, 185, 185)
        rect(0, 0, 675, 135) # draws sky
        
        textSize(10)
        fill(255, 255, 255)
        text("Score: %s"%(player.score), 10, 15) # draws score to screen
        
        fill(255, 0, 0)
        textSize(50)
        text("Game Over", 117.5, 300) # draws game over text to screen
        
    
    elif stage.mode == 'menu': # if on main menu
        player.shieldTimer = millis() # updates shield timer to current time (for when game starts)
        
        
    
def keyPressed():
    if stage.mode == 'play': # if game is under way
        if (key == 'A') or (key == 'a'): # moves player left
            player.move('a', stage.dug)
            stage.sounds["walkMusic"].play() # plays Dig Dug's walking music

            if player.lastMoved == 0: # sets the time that the player started to move
                player.lastMoved = millis() 
            
            if millis() - player.lastMoved >= (stage.sounds["walkMusic"].length() + 100): # checks if it is time to rewind sound
                stage.sounds["walkMusic"].rewind() # rewinds Dig Dug's walking music
        
        elif (key == 'D') or (key == 'd'): # moves player right
            player.move('d', stage.dug)
            stage.sounds["walkMusic"].play() # plays Dig Dug's walking music

                
            if player.lastMoved == 0: # sets the time that the player started to move
                player.lastMoved = millis()
            
            if millis() - player.lastMoved >= (stage.sounds["walkMusic"].length() + 100): # checks if it is time to rewind sound
                stage.sounds["walkMusic"].rewind() # rewinds Dig Dug's walking music
        
        elif (key == 'S') or (key == 's'): # moves player down
            player.move('s', stage.dug)
            stage.sounds["walkMusic"].play() # plays Dig Dug's walking music
            
                
            if player.lastMoved == 0: # sets the time that the player started to move
                player.lastMoved = millis()
            
            if millis() - player.lastMoved >= (stage.sounds["walkMusic"].length() + 100): # checks if it is time to rewind sound
                stage.sounds["walkMusic"].rewind() # rewinds Dig Dug's walking music
        
        elif (key == 'W') or (key == 'w'): # moves player up
            player.move('w', stage.dug)
            stage.sounds["walkMusic"].play() # plays Dig Dug's walking music
            
                
            if player.lastMoved == 0: # sets the time that the player started to move
                player.lastMoved = millis()
            
            if millis() - player.lastMoved >= (stage.sounds["walkMusic"].length() + 100): # checks if it is time to rewind sound
                stage.sounds["walkMusic"].rewind() # rewinds Dig Dug's walking music
        
        else:
            stage.sounds["walkMusic"].pause() # pauses Dig Dug's walking music
            stage.sounds["walkMusic"].rewind() # rewinds Dig Dug's walking music

def keyReleased():
    stage.sounds["walkMusic"].pause() # pauses & rewinds sound on key release
    stage.sounds["walkMusic"].rewind()
    
    
        
def mouseClicked():
    global stage, player
    
    if (stage.mode == 'play') and not(player.shieldEnabled): # if game has started
        if not(player.weapon): # checks if enemy is in range
            stage.sounds["shoot"].play() # plays shooting sound
            stage.sounds["shoot"].rewind() # rewinds shooting sound
            for mob in range(len(stage.enemies)):
                stage.enemies[mob].checkHit(player)
            
        player.attack(millis()) # if mouse is clicked during gameplay, the player attacks
        
        
    elif stage.mode == 'menu': # main menu
        if ((285 <= mouseX <= 385) and (380 <= mouseY <= 405)) and not(stage.invalidName): # starts game
            stage.mode = 'play'
            player.name = "".join([stage.possibleCharacters[stage.name[n]] for n in range(3)]) # sets the player's name
            
            stage.sounds["start"].pause() # stops stating jingle (if still playing)
            stage.sounds["start"].rewind() # rewinds starting jingle
            
            stage.sounds["play"].play() # plays starting sound
            stage.sounds["play"].rewind() # rewinds starting sound
            
            
        
        elif (210 <= mouseX <= 455) and (450 <= mouseY <= 475): # goes to high score screen
            stage.mode = 'scores'
            
            stage.scoreAllocation(player) # sorts & allocates scores 
        
        elif (0 <= mouseX <= 180) and (790 <= mouseY <= 815): # goes to instruction screen
            stage.mode = 'instructions'
         
         # player name change
        elif (547 <= mouseY <= 557):
                if (390 <= mouseX <= 405): # right up
                    stage.name[2] -= 1
                    if stage.name[2] < 0:
                        stage.name[2] = len(stage.possibleCharacters) - 1
                
                elif (322 <= mouseX <= 336): # middle up
                    stage.name[1] -= 1
                    if stage.name[1] < 0:
                        stage.name[1] = len(stage.possibleCharacters) - 1
                 
                
                elif (252 <= mouseX <= 268): # left up
                    stage.name[0] -= 1
                    if stage.name[0] < 0:
                        stage.name[0] = len(stage.possibleCharacters) - 1
        
        elif (610 <= mouseY <= 620):
            if (390 <= mouseX <= 405): # right down
                stage.name[2] += 1
                if stage.name[2] >= len(stage.possibleCharacters):
                    stage.name[2] = 0
            
            elif (322 <= mouseX <= 336): # middle down
                stage.name[1] += 1
                if stage.name[1] >= len(stage.possibleCharacters):
                    stage.name[1] = 0
            
            elif (252 <= mouseX <= 268): # left up
                stage.name[0] += 1
                if stage.name[0] >= len(stage.possibleCharacters):
                    stage.name[0] = 0
            

    
    elif stage.mode == 'scores': # return to menu from high scores
        stage.mode = 'menu'
    
    elif stage.mode == 'gameOver': # reset game from game over screen (& go to menu)
        player = Miner(spriteSheet, loadImage("shield.png"), minim)
        stage = Level(spriteSheet, minim)
        stage.stageLoad(0)
    
    elif stage.mode == 'instructions':
        stage.mode = 'menu' # returns to menu on click on instructions screen

# Created by Ryan B. Green in May/June 2019
    