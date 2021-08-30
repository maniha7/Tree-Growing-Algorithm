import GUI
import pygame
import time


window = GUI.window()
running = True
updateTime = .02
totalTime = 0
frames = 0
window.update(window)

while running:
    for event in window.getEvent():
        #Close button control
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                window.reset()


            # SPEED CONTROLS
            if event.key == pygame.K_RIGHT and updateTime >0.011:
                updateTime -= .01
            elif event.key == pygame.K_RIGHT and updateTime <=0.011:
                updateTime =0
            if event.key == pygame.K_LEFT and updateTime < .51111:
                updateTime += .01




    if window.frozen == False:

        frames+=1
        tic = time.perf_counter()
        window.update(window)
        toc = time.perf_counter()
        totalTime += toc-tic
        print("Frame time: ", toc-tic)
        print("Avg time: ", totalTime/frames)
    time.sleep(updateTime)