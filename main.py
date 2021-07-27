from asyncio.tasks import current_task
import discord, os, time, random
from discord import mentions, VoiceChannel
from discord import message

TOKEN = os.environ['Discord Token']

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("<help | https://sites.google.com/view/GalacticBank"))
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    if message.content[:5].lower() == "<help":
        time.sleep(1)

        await message.delete()
        
        if message.author.guild_permissions.administrator:
            # Admin only
            embedVarAdmin = discord.Embed(title="List of admin commands", color=0x00ff00)
            embedVarAdmin.add_field(name="<investment ['@name'] ['number']", value="Adds 'number' funds to '@name's account")
            embedVarAdmin.add_field(name="<balance ['@name']", value="Returns the balance of '@name's account")
            embedVarAdmin.add_field(name="<withdraw ['@name'] ['number']", value="Withdraws 'number' funds from '@name's account")
            embedVarAdmin.add_field(name="<interest", value="Cycles through all accounts adding a 10% interest")

            await message.channel.send(embed=embedVarAdmin)
        
        # Anyone
        embedVarAnyone = discord.Embed(title="List of commands", color=0x00ff00)
        embedVarAnyone.add_field(name="<help", value = "Shows a list of commands")
        embedVarAnyone.add_field(name="<balance ['@name']", value="Returns the balance if '@name's account")

        await message.channel.send(embed=embedVarAnyone)
    
    elif message.content[:11].lower() == "<investment" and message.author.guild_permissions.administrator:
        arguments = message.content[12:]
        find = arguments.find(" ")

        user = f"{arguments[1:find-1]}"

        amount = int(arguments[find:])
        
        try:
            path = f"Investments/{str(user)}"
            file = open(f"{path}", "r")
            currentAmount = int(file.read())
            file.close()
        
        except:
            path = f"Investments/{str(user)}"
            file = open(f"{path}", "w")
            file.write("0")
            currentAmount = 0
            file.close()

        newAmount = currentAmount + amount

        path = f"Investments/{str(user)}"
        file = open(f"{path}", "w")
        file.write(str(newAmount))
        file.close()

        await message.channel.send(f"Invested {amount} credits in <{user}>'s account")


    elif message.content[:8].lower() == "<balance":
        arguments = message.content[9:]

        length = len(arguments)

        user = arguments[1:length-1]

        if str(message.author.id) == str(user[2:]) or message.author.guild_permissions.administrator:
            try:
                file = open(f"Investments/{user}", "r")
                balance = int(file.read())
                file.close()
            except:
                file = open(f"Investments/{user}", "w")
                file.write("0")
                balance = 0
                file.close()

            await message.channel.send(f"<{user}> : **{balance}**")
        
        else:
            await message.channel.send(f"{message.author.mention} this is not your account!")

    elif message.content[:9].lower() == "<withdraw" and message.author.guild_permissions.administrator:
        arguments = message.content[10:]

        find = arguments.find(" ")

        user = arguments[1:find-1]
        amount = int(arguments[find:])

        try:
            file = open(f"Investments/{user}", "r")
            currentBalance = int(file.read())
            file.close()
        except:
            file = open(f"Investments/{user}", "w")
            file.write("0")
            currentBalance = 0
            file.close()
        
        if currentBalance < amount:
            await message.channel.send(f"<{user}> does not have enough in thier account!")
        
        else:
            file = open(f"Investments/{user}", "w")
            newBalance = currentBalance - amount
            file.write(str(newBalance))
            file.close()
            
            await message.channel.send(f"Withdrawed {amount} from <{user}>'s account")
        
    elif message.content.lower() == "<interest" and message.author.guild_permissions.administrator:
        directory = os.fsencode("Investments")

        for account in os.listdir(directory):
            file = open(f"Investments/{account.decode()}", "r")
            balance = int(file.read())
            file.close()

            newBalance = balance * 1.1

            file = open(f"Investments/{account.decode()}", "w")
            file.write(str(int(round(newBalance, 0))))
            file.close()

        await message.channel.send("Done!")



async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise

        
        



client.run(TOKEN)
