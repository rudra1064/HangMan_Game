import random
import pygame
import requests
import time

pygame.init()

# screen
screen=pygame.display.set_mode((1500, 800))
pygame.display.set_caption("HangMan Game")
icon=pygame.image.load("hangman-game.png")
pygame.display.set_icon(icon)

#font
white=(255, 255,255)
font= pygame.font.Font(None,48)
bigfont= pygame.font.Font(None,100)

#Music
pygame.mixer.init()
correct_sound="start.mp3"
wrong_sound="wrong.mp3"
win_sound="masterbgm.mp3"
game_over_sound="lost.mp3"

#random word function
def random_word():
    word=requests.get("https://random-word-api.herokuapp.com/word").json()[0]
    # word=["mango","tiger"]
    # word=random.choice(word)
    meaning=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()[0]["meanings"][0]["definitions"][0]["definition"]
    return word,meaning

# Hangman Drawing Function
def HangmanDraw(stage, shift=0):
    pygame.draw.line(screen,white,(100,500),(200,500),5)  #base
    pygame.draw.line(screen,white,(100,500),(100,200),5)  #pole
    pygame.draw.line(screen,white,(100,200),(200,200),5)  #head
    pygame.draw.line(screen,white,(200,200),(200,250),5)  #rope

    if stage >= 1:
        pygame.draw.circle(screen,white,(200,275),25,5)  #head
    if stage >= 2:
        pygame.draw.line(screen,white,(200,300),(200,375), 5)  #body
    if stage >= 3:
        pygame.draw.line(screen,white,(200,325),(170, 350 - shift),5)  #left arm 
    if stage >= 4:
        pygame.draw.line(screen,white,(200,325),(230, 350 - shift),5)  #right arm 
    if stage >= 5:
        pygame.draw.line(screen,white,(200,375),(170, 425 - shift),5)  #left leg 
    if stage >= 6:
        pygame.draw.line(screen,white,(200,375),(230, 425 - shift),5)  #right leg 

# Display Word Function
def display_word(word, guessed_letters):
    display_text=" ".join([letter if letter in guessed_letters else "_" for letter in word])
    text =bigfont.render(display_text, True, white)
    screen.blit(text, (650, 500))

# Celebration Function
def celebration(word):
    pygame.mixer.music.load(win_sound)
    pygame.mixer.music.play()
    for _ in range(10):
        screen.fill((0, 0, 0))
        shift=random.choice([-30, 30])
        HangmanDraw(6, shift)
        win_text =font.render(f"You won! The word was: {word}",True,white)
        screen.blit(win_text,(500, 200))
        pygame.display.update()
        time.sleep(0.2)
    time.sleep(2)

#game over function
def game_over(word):
    pygame.mixer.music.load(game_over_sound)
    pygame.mixer.music.play()
    for _ in range(5):
        screen.fill((0, 0, 0))
        game_over_text= font.render(f"Game Over! The word was: {word}",True,white)
        screen.blit(game_over_text,(500, 200))
        pygame.display.update()
        time.sleep(1)
    time.sleep(2)

# main 
def hangman():
    attempts=6
    guessed_letters=set()
    word, hint=random_word()
    print(word)
    running=True

    while running:
        screen.fill((0, 0, 0))

        hint_txt= font.render(f"Hint: {hint}", True, white)
        screen.blit(hint_txt,(50, 50))

        lives_txt= font.render(f"Lives: {attempts}", True, white)
        screen.blit(lives_txt,(1300, 150))

        HangmanDraw(6 - attempts)
        display_word(word, guessed_letters)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():  
                    guess = event.unicode.lower()
                    if guess in guessed_letters:
                        print("Already guessed")
                    elif guess in word:
                        pygame.mixer.music.load(correct_sound)
                        pygame.mixer.music.play()
                        guessed_letters.add(guess)
                        if all(letter in guessed_letters for letter in word):
                            print("You won !")
                            celebration(word)
                            running = False
                    else:
                        pygame.mixer.music.load(wrong_sound)
                        pygame.mixer.music.play()
                        guessed_letters.add(guess)
                        attempts -= 1
                        if attempts == 0:
                            print("Game Over ! The word was:", word)
                            game_over(word)
                            running = False
        
        pygame.display.update()

hangman()
pygame.quit()
