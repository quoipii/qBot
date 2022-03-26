import discord
import discord.ext
from discord.ext import commands, tasks
from datetime import datetime
import pathlib
import os
from os import listdir
from os.path import isfile, join
import random
import requests
from PIL import Image, ImageDraw, ImageFont
import skimage.io as skio
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import *

#For qDictionary
illegalCharacters = '\/:"?<>'
seperator = "983274923857684#^#@7632%#987452398578@94752393$784236489576298"

#For satellite stuff
bands = ["swir2","swir1","sdev","red","green","blue","nir","edev","count","bcdev"]
cmaps = "flag, prism, ocean, gist_earth, terrain, gist_stern, gnuplot, gnuplot2, CMRmap, cubehelix, brg, gist_rainbow, rainbow, jet, turbo, nipy_spectral, gist_ncar, viridis, plasma, inferno, magma, cividisGreys, Purples, Blues, Greens, Oranges, Reds, YlOrBr, YlOrRd, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn, PiYG, PRGn, BrBG, PuOr, RdGy, RdBu, RdYlBu, RdYlGn, Spectral, coolwarm, bwr, seismic, twilight, twilight_shifted, hsv"

#For Letters and Numbers
big = [100, 100, 75, 75, 50, 50, 25, 25, 10, 10]
small = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9]
recursionDepth = 0
def getCombos(stateList, target, equList=None):
    global recursionDepth

    boardStates = []
    equStates = []

    #addition
    stateCount = 0
    for numList in stateList:
        num1count = 0
        for number in numList:
            num2count = 0
            for number2 in numList:
                #print(f"Comparing {num1count} and {num2count}")
                if num1count != num2count and recursionDepth < 5:
                    tempBoard = [i for i in numList]                    
                    tempBoard.remove(number)
                    tempBoard.remove(number2)
                    tempBoard.append(number+number2)
                    boardStates.append(tempBoard)
                    
                    if equList == None:
                        tempEqu = [str(i) for i in numList]
                        tempEqu.remove(str(number))
                        tempEqu.remove(str(number2))
                        tempEqu.append(f"({number} + {number2})")
                        equStates.append(tempEqu)
                    else:
                        tempEqu = [str(i) for i in equList[stateCount]]
                        tempEqu.remove(str(equList[stateCount][num1count]))
                        tempEqu.remove(str(equList[stateCount][num2count]))
                        tempEqu.append(f"({equList[stateCount][num1count]} + {equList[stateCount][num2count]})")
                        equStates.append(tempEqu)

                num2count += 1
            num1count += 1
        stateCount += 1

    #subtraction
    stateCount = 0
    for numList in stateList:
        num1count = 0
        for number in numList:
            num2count = 0
            for number2 in numList:
                #print(f"Comparing {num1count} and {num2count}")
                if num1count != num2count and number-number2 > 0 and number-number2 != number2 and recursionDepth < 5:
                    tempBoard = [i for i in numList]                    
                    tempBoard.remove(number)
                    tempBoard.remove(number2)
                    tempBoard.append(number-number2)
                    boardStates.append(tempBoard)
                    
                    if equList == None:
                        tempEqu = [str(i) for i in numList]
                        tempEqu.remove(str(number))
                        tempEqu.remove(str(number2))
                        tempEqu.append(f"({number} - {number2})")
                        equStates.append(tempEqu)
                    else:
                        tempEqu = [str(i) for i in equList[stateCount]]
                        tempEqu.remove(str(equList[stateCount][num1count]))
                        tempEqu.remove(str(equList[stateCount][num2count]))
                        tempEqu.append(f"({equList[stateCount][num1count]} - {equList[stateCount][num2count]})")
                        equStates.append(tempEqu)

                num2count += 1
            num1count += 1
        stateCount += 1

    #multplication
    stateCount = 0
    for numList in stateList:
        num1count = 0
        for number in numList:
            num2count = 0
            for number2 in numList:
                #print(f"Comparing {num1count} and {num2count}")
                if num1count != num2count and number != 1 and number2 != 1:
                    tempBoard = [i for i in numList]                    
                    tempBoard.remove(number)
                    tempBoard.remove(number2)
                    tempBoard.append(number*number2)
                    boardStates.append(tempBoard)
                    
                    if equList == None:
                        tempEqu = [str(i) for i in numList]
                        tempEqu.remove(str(number))
                        tempEqu.remove(str(number2))
                        tempEqu.append(f"({number} * {number2})")
                        equStates.append(tempEqu)
                    else:
                        tempEqu = [str(i) for i in equList[stateCount]]
                        tempEqu.remove(str(equList[stateCount][num1count]))
                        tempEqu.remove(str(equList[stateCount][num2count]))
                        tempEqu.append(f"({equList[stateCount][num1count]} * {equList[stateCount][num2count]})")
                        equStates.append(tempEqu)

                num2count += 1
            num1count += 1
        stateCount += 1

    #division
    stateCount = 0
    for numList in stateList:
        num1count = 0
        for number in numList:
            num2count = 0
            for number2 in numList:
                #print(f"Comparing {num1count} and {num2count}")
                if num1count != num2count and number2 > 0 and number % number2 == 0 and number/number2 != number2:
                    tempBoard = [i for i in numList]                    
                    tempBoard.remove(number)
                    tempBoard.remove(number2)
                    tempBoard.append(number/number2)
                    boardStates.append(tempBoard)
                    
                    if equList == None:
                        tempEqu = [str(i) for i in numList]
                        tempEqu.remove(str(number))
                        tempEqu.remove(str(number2))
                        tempEqu.append(f"({number}/{number2})")
                        equStates.append(tempEqu)
                    else:
                        tempEqu = [str(i) for i in equList[stateCount]]
                        tempEqu.remove(str(equList[stateCount][num1count]))
                        tempEqu.remove(str(equList[stateCount][num2count]))
                        tempEqu.append(f"({equList[stateCount][num1count]} / {equList[stateCount][num2count]})")
                        equStates.append(tempEqu)

                num2count += 1
            num1count += 1
        stateCount += 1

    #print(recursionDepth)
    for equBoard in equStates:
        for equation in equBoard:
            try:
                if eval(equation) == target:
                    return equation
            except:
                pass

    if len(boardStates[0]) != 1:
        recursionDepth += 1
        return getCombos(boardStates, target, equStates)
    return False

#gives me members back
intents = discord.Intents().all()
intents.members = True

client = commands.Bot(intents=intents,command_prefix=">",help_command=None,case_insensitive=True)

#------HELP------#
@client.command()
async def help(ctx):
    #Did this so I can see the command better
    helpText = [
        "**PREFIX: >**",
        "",
        "**qDictionary**", #-----------------------------------------------
        "> define [word] | [definition]",
        "Defines a word with the given definition.",
        "> read [word]",
        "Reads all definitions for a given word",
        "> allWords",
        "Prints all defined words",
        "",
        "**Memes**",#-----------------------------------------------
        "> meme [title] | [subtext] | [image url]",
        "Generates a meme with the provided image and text.",
        "",
        "**Satellite Imagery**",
        "> satellite [year] | [x] [y] | [band] | [colourmap *OPTIONAL].",
        "*Example: >satellite 2016 | x40 y33 | swir1 | magma*",
        "> satHelp",
        "A help command to elaborate on the requirements of the >satellite command.",
        "",
        "**Letters and Numbers (Numbers game only)**",
        "> numgame [integer] big [integer] small",
        "Simulates the numbers game from Letters and Numbers/Countdown",
        "Big numbers are 10, 25, 50, 75 and 100 whilst small numbers range from 1 to 9.",
        "You must choose a total of exactly 6 big and small numbers (e.g: 2 big 4 small)",
        "*Example: >numgame 2 big 4 small*",
        "> numtimed [integer] big [integer] small",
        "Same premise as >numgame, however this command times you and keeps the answer secret until you guess correctly using >numguess or type 'give up'",
        "> numguess ||equation|\|",
        "Used for submitting answers to a started >numtimed game",
        "Valid answers may include any provided numbers and basic operators (division, multiplication, addition and subtraction). You may also type 'give up' to give up."
    ]

    helpTextString = "\n".join(helpText)
    embed = discord.Embed(title="ALL COMMANDS:", description=helpTextString, color=discord.Color.red())
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    activity = discord.Game(name=">help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("qBot is active.")

@client.event
async def on_message(message):
    if int(message.channel.id) != 948515142935662602: #Enter the user ID of any text channel that the bot shouldnt interact with
        await client.process_commands(message)

#------Anti-LeagueOfLegends------#
@tasks.loop(seconds=5)
async def checkActivity():
    global datetimeArchive, exerciseMsgs
    await client.wait_until_ready()
    guild = client.get_guild(890858400047595520) #Enter the guild ID of the server you want to ban league of legends players from

    for member in guild.members:
        activityString = ""
    
        if len(member.activities) == 0:
            pass
        
        else:
            for activity in member.activities:
                activityString += str(activity) 
            if "league of legends" in activityString.lower() :
                channel = await member.create_dm()
                await channel.send("https://tenor.com/view/league-league-of-legends-lo-l-uninstall-league-5easy-steps-gif-21441913")    
                print(f"{member} was caught playing League. {member.activities[0]}.")
                await member.ban(reason="Banned for cringe", delete_message_days=0)

#------MEME GEN!!------#
@client.command()
async def meme(ctx, *args):
    memeInput = " ".join(args)
    title = ""
    subtext = ""
    if len(memeInput.split("|")) != 3:
        await ctx.channel.send("Please follow this format: >meme title | subtext | image url")
    else:
        title = memeInput.split("|")[0].strip()
        subtext = memeInput.split("|")[1].strip()
        url = memeInput.split("|")[2].strip()

        bgW, bgH = (800, 600)
        background = Image.new(mode="RGB", size=(bgW, bgH)) #Make bg
        memeImg = requests.get(url).content #Get image from their message
        memeName = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\memeImgs\\{memeName}.png', 'wb') as saveMemeImg:
            saveMemeImg.write(memeImg)
        
        resizeSize = (700, 300)
        memeImg = Image.open(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\memeImgs\\{memeName}.png')
        memeImg = memeImg.resize(resizeSize)
        Image.Image.paste(background,memeImg, (50,50))
        memeFinal = ImageDraw.Draw(background)
        memeFinal.rectangle([(40,40),(760,360)])

        bounding_box_title = [0, 400, 800, 425]
        tx1, ty1, tx2, ty2 = bounding_box_title
        bounding_box_subtext = [0, 475, 800, 525]
        sx1, sy1, sx2, sy2 = bounding_box_subtext

        #Write text
        font = ImageFont.truetype(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\fonts\\arial.ttf', 54) 
        w, h = memeFinal.textsize(title, font=font)
        x = (tx2 - tx1 - w)/2 + tx1
        y = (ty2 - ty1 - h)/2 + ty1
        memeFinal.text((x, y), title, font=font, align='center', fill="white") #DRAW TITLE

        font = ImageFont.truetype(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\fonts\\arial.ttf', 30) 
        w, h = memeFinal.textsize(subtext, font=font)
        x = (sx2 - sx1 - w)/2 + sx1
        y = (sy2 - sy1 - h)/2 + sy1
        memeFinal.text((x, y), subtext, font=font, align='center', fill="white") #DRAW SUBTEXT

        background.save(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\finishedMemes\\{memeName}.png')
        with open(f'{pathlib.Path().resolve()}\memeGen\\blackbox\\finishedMemes\\{memeName}.png', 'rb') as finalMemeImage:
            picture = discord.File(finalMemeImage)
            await ctx.channel.send(file=picture)


#------Satellite Images------#
def checkY(x, band): #Will check from the middle out
    print('a')
    y = 29
    yselection = []
    end = False
    count = 1

    while end == False:
        webPage = requests.get(f"https://data.dea.ga.gov.au/derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/{x}/y{y}/2020--P1Y/ga_ls8c_nbart_gm_cyear_3_{x}y{y}_2020--P1Y_final_{band}.tif").content
        
        if not "The specified key does not exist." in str(webPage):
            yselection.append(y)
        else:
            if len(yselection) > 4:
                end = True
        if len(yselection) > 10:
            end = True
        if y == 0:
            end = True
        if count > 0:
            count += 1
            count *= -1
        else:
            count -= 1
            count *= -1
        y += count 
        #print(y)
    return yselection
        
@client.command()
async def satellite(ctx, *args):
    argsFull = " ".join(args).split("|")
    argLengths = [3,4]
    
    if len(argsFull) in argLengths:
        if len(argsFull) == 4:
            cmap = argsFull[3].strip()
        else:
            cmap = "magma"

        year = argsFull[0].strip().lower()
        coords = argsFull[1].strip().lower()
        whatBand = argsFull[2].strip().lower()

        if argsFull[1].strip().lower() == "random":
            year = "2020" #to avoid errors for non existent years
            whatX = "x" + str(random.choice(range(10,54)))
            print("x: " + str(whatX))
            await ctx.channel.send("Choosing valid coordinates.... this may take a while")
            possibleY = checkY(whatX, whatBand)
            print(possibleY)
            whatY = "y"+str(random.choice(possibleY))
        else:
            whatX = coords.split()[0]
            whatY = coords.split()[1]
        

        tifFile = requests.get(f"https://data.dea.ga.gov.au/derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/{whatX}/{whatY}/{year}--P1Y/ga_ls8c_nbart_gm_cyear_3_{whatX}{whatY}_{year}--P1Y_final_{whatBand}.tif")
        print(f"https://data.dea.ga.gov.au/derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/{whatX}/{whatY}/{year}--P1Y/ga_ls8c_nbart_gm_cyear_3_{whatX}{whatY}_{year}--P1Y_final_{whatBand}.tif")
        #https://data.dea.ga.gov.au/derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/x51/y33/2017--P1Y/ga_ls8c_nbart_gm_cyear_3_x51y33_2017--P1Y_final_nir.tif
        print("tif recieved")
        open(f'{pathlib.Path().resolve()}\\landsatStuff\\band.tif', 'wb').write(tifFile.content)
        print("tif saved")

        if True:
            image = skio.imread(f'{pathlib.Path().resolve()}\\landsatStuff\\band.tif', plugin="tifffile")
            imageCopy = skio.imread(f'{pathlib.Path().resolve()}\\landsatStuff\\band.tif', plugin="tifffile") #test copy, seeing if .ravel() ruins the OG
            imageFlat = imageCopy.ravel()
            imageFlat.sort()

            upperRange = imageFlat[10137600].item()
            lowerRange = imageFlat[102400].item()

            rebuiltArray = np.clip(image, lowerRange, upperRange)#  --- to use this again, just replace "image" in plt.imshow(image, cmap=cmap) with rebuiltArray

            imgPlot = plt.imshow(rebuiltArray, cmap=cmap)
            plt.colorbar(mappable=imgPlot)
            plt.savefig(f"{pathlib.Path().resolve()}\\landsatStuff\\final.png")
            await ctx.send(f"Image from {whatX}, {whatY}, during {year}. Showing {whatBand}.\nFor more info, visit https://data.dea.ga.gov.au/?prefix=derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/", file=discord.File(f"{pathlib.Path().resolve()}\\landsatStuff\\final.png"))

            #imgPlot.clear()
            plt.clf()
            print("Done")
        #except:
        #    await ctx.channel.send("Command execution failed!")

    else:
        await ctx.channel.send("Please follow this format: >satellite [year] | [x] [y] | [band] | [colourmap *OPTIONAL].```Example: >satellite 2016 | x40 y33 | swir1```")

@client.command()
async def satHelp(ctx):
    satHelpStr = [
        "**Possible band values:**",
        ", ".join(bands),
        "",
        "**Coordinate help:**",
        "Valid coordinate pairs can be determined via https://data.dea.ga.gov.au/?prefix=derivative/ga_ls8c_nbart_gm_cyear_3/3-0-0/",
        "First click on a given x coordinate, then follow it up with any y coordinates you can then see. This will be a valid pair.",
        "",
        "**Years:**",
        "Valid years CAN range from 2013 to 2020, at MAXIMUM. If earlier years don't work, try more recent ones.",
        "",
        "Colour maps:",
        "This is the fun bit, this is essentially what colouts the graph will plot.",
        "Here is a list of all available colourmaps:",
        f"*{cmaps}*"
    ]
    embed = discord.Embed(title="SATELLITE COMMAND HELP:", description="\n".join(satHelpStr), color=discord.Color.blue())
    await ctx.send(embed=embed)

#------qDictionary------#
@client.command()
async def define(ctx, *args):
    global seperator

    defWord = ""
    definition = ""
    command = " ".join(args)
    illegal = False
    isDef = False
    for word in command.split():
        for letter in word:
            if letter in illegalCharacters and isDef == False:
                illegal = True
        if word == "|":
            isDef = True
        elif isDef == False:
            defWord += word + " "
        else:
            definition += word + " "
    defWord = defWord[:-1]
    definition = definition[:-1]
    word = defWord.lower()
 
    if len(definition) == 0 or len(word) == 0:
        await ctx.channel.send("Please follow this format: >define word | definition.")
    if illegal == True:
        await ctx.channel.send('Please avoid using the characters /\:"?<>')
    else:
        with open(f"{pathlib.Path().resolve()}\qDictionary\definitions\{word}.txt", "a") as wordDef:
            wordDef.write(definition)
            wordDef.write(f"\n{seperator}")

        now = datetime.now()
        time = now.strftime("%Y/%m/%d %H:%M:%S")
        await ctx.channel.send(f"{word} has been successfully defined!")
        print(f"{ctx.author.name} just defined {word} as {definition}. {time}")

@client.command()
async def read(ctx, *args):
    global seperator

    word = (" ".join(args)).lower()
    if len(word) == 0:
        await ctx.channel.send("Please enter a word to read.")
    else:
        if os.path.exists(f"{pathlib.Path().resolve()}\qDictionary\definitions\{word}.txt"):
            message = f"{word} is defined as:\n"
            count = 1
            with open(f"{pathlib.Path().resolve()}\qDictionary\definitions\{word}.txt", "r") as wordDef:
                definitions = wordDef.read().split(seperator)

            definitions = definitions[:-1]
            for meaning in definitions:
                message += f"{count}: {meaning}"
                count += 1
            
            await ctx.channel.send(message)
        else:
            await ctx.channel.send("That word has not been defined!")

@client.command()
async def allWords(ctx):
    onlyfiles = ["- "+f.split(".")[0] for f in listdir(f"{pathlib.Path().resolve()}\qDictionary\definitions") if isfile(join(f"{pathlib.Path().resolve()}\qDictionary\definitions", f))]
    onlyfiles = "\n".join(onlyfiles)
    fileString = f"ALL DEFINED WORDS/PHRASES:\n{onlyfiles}"
    if len(fileString) >= 2000:
        splitMessage = [fileString[i:i+1800] for i in range(0, len(fileString), 1800)]
        for wordList in splitMessage:
            await ctx.channel.send(wordList)
    else:
        await ctx.channel.send(fileString)

#------Letters and Numbers------#
@client.command()
async def numgame(ctx, *args):
    fullInput = (" ".join(args)).lower()
    justNum = ((fullInput.replace("big", "").replace("small", "")).strip()).split()
    
    if len(justNum) == 2:
        if justNum[0].isdigit() and justNum[1].isdigit() and int(justNum[0]) + int(justNum[1]) == 6:
            await ctx.send(f"Processing command . . .")
            
            listInputTemp = []
            bigCopy = [i for i in big]
            smallCopy = [i for i in small]
            for i in range(0,int(justNum[0])):
                chosenBig = random.choice(bigCopy)
                listInputTemp.append(chosenBig)
                bigCopy.remove(chosenBig)

            for i in range(0,int(justNum[1])):
                chosenSmall = random.choice(smallCopy)
                listInputTemp.append(chosenSmall)
                smallCopy.remove(chosenSmall)
            
            strInput = []
            intInput = []
            strInput.append([str(i) for i in listInputTemp])
            intInput.append([i for i in listInputTemp])
            print(strInput)
            
            isPossible = False
            while isPossible == False:
                targetNum = random.choice(range(100,1000))
                print(f"Testing target number of {targetNum}")
                isPossible = getCombos(intInput, targetNum, strInput)

            formatNums = ", ".join([str(i) for i in listInputTemp])
            await ctx.send(f"Using `{formatNums}`, try and reach `{targetNum}`.\nThe solution is: ||`{isPossible[1:-1]}`||")
        else:
            await ctx.send("Please enter two integers (NOT IN WORD FORM) that add up to 6.")
    else:
        await ctx.send("Please follow the format: >numgame [digit] big [digit] small.")

@client.command()
async def numtimed(ctx, *args):
    fullInput = (" ".join(args)).lower()
    justNum = ((fullInput.replace("big", "").replace("small", "")).strip()).split()
    
    if len(justNum) == 2:
        if justNum[0].isdigit() and justNum[1].isdigit() and int(justNum[0]) + int(justNum[1]) == 6:
            await ctx.send(f"Processing command . . .")
            
            listInputTemp = []
            bigCopy = [i for i in big]
            smallCopy = [i for i in small]
            for i in range(0,int(justNum[0])):
                chosenBig = random.choice(bigCopy)
                listInputTemp.append(chosenBig)
                bigCopy.remove(chosenBig)

            for i in range(0,int(justNum[1])):
                chosenSmall = random.choice(smallCopy)
                listInputTemp.append(chosenSmall)
                smallCopy.remove(chosenSmall)
            
            strInput = []
            intInput = []
            strInput.append([str(i) for i in listInputTemp])
            intInput.append([i for i in listInputTemp])
            print(strInput)
            
            isPossible = False
            while isPossible == False:
                targetNum = random.choice(range(100,1000))
                print(f"Testing target number of {targetNum}")
                isPossible = getCombos(intInput, targetNum, strInput)
            formatNums = ", ".join([str(i) for i in listInputTemp])
            
            #Save this in a savefile
            with open(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt", "a+") as saveFile:
                saveFile.write(f"{datetime.today().timestamp()}\n{formatNums}\n{targetNum}\n{isPossible[1:-1]}")

            await ctx.send(f"Using `{formatNums}`, try and reach `{targetNum}`.\nType >numsubmit ||answer|\|")
        else:
            await ctx.send("Please enter two integers (NOT IN WORD FORM) that add up to 6.")
    else:
        await ctx.send("Please follow the format: >numgame [digit] big [digit] small.")

@client.command()
async def numsubmit(ctx, *args):
    if os.path.exists(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt"):
        ans = " ".join(args).replace(" ", "").replace("|","")
        ansNums = ans.replace("*","#").replace("/","#").replace("+","#").replace("-","#").replace("(","#").replace(")","#")

        if ansNums.replace("#","").isdigit():
            with open(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt", "r") as userSave:
                totalSave = userSave.read().split("\n")
                numList = totalSave[1].split(", ")
                target = int(totalSave[2])
                solution = totalSave[3]
                timeStarted = int(round(float(totalSave[0])))

            valid = True
            for usedNum in ansNums.split("#"):
                if len(usedNum) < 1:
                    pass
                elif not usedNum in numList:
                    valid = False
                    print(f"{usedNum} is not in {numList}")
                else:
                    numList.remove(usedNum)
            
            if valid == True:
                if eval(ans) == target:
                    timeTaken = round((datetime.today().timestamp() - timeStarted)/60)
                    await ctx.send(f"You solved it in approximately {timeTaken} minutes!\nI used ||{solution}|| as a solution.")
                    open(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt", "w").close()
                else:
                    await ctx.send(f"This guess doesn't seem to have the right answer...")
            else:
                await ctx.send(f"You seem to have used some numbers you shouldn't have been able to use.")
        
        elif ans.lower() == "give up":
            with open(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt", "r") as userSave:
                totalSave = userSave.read().split("\n")
                numList = totalSave[1].split(", ")
                target = int(totalSave[2])
                solution = totalSave[3]
                timeStarted = int(round(float(totalSave[0])))

            timeTaken = round((datetime.today().timestamp() - timeStarted)/60)
            await ctx.send(f"You gave up in approximately {timeTaken} minutes!\nYou can reach {target} using {','.join(numList)} by calculating ||{solution}||")
            open(f"{pathlib.Path().resolve()}\Letters and Numbers\\numSaves\{ctx.author.id}.txt", "w").close()
        
        else:
            await ctx.send("You may have formatted your answer wrong, do not use any symbols other than /, +, *, -, ( and )")
    else:
        await ctx.send("I don't see a save file under your user ID...\nIf you have started a game and believe this is an error, ping Moss.")
        
checkActivity.start()
client.run("""ENTER YOUR AUTH TOKEN HERE - YOU CAN FIND IT WHEN YOU MAKE A BOT APP IN THE DISCORD DEVELOPER PORTAL""")