import discord, paramiko
from discord.ext import commands
from data import *

x = '[:x:] '
s = '[:white_check_mark:] '
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password, port=port)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="ssh bot", url="https://roblox.com/"))
    print("READY")

#commands            
@client.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong")

@client.slash_command()
async def connect(inter):
    global ssh
    try:
        ssh.exec_command('ls')
        await inter.response.send_message(x+"Connection already exists !")    
    except:
        ssh.connect(hostname=hostname, username=username, password=password, port=port)
        await inter.response.send_message(s+"Connected back !")

@client.slash_command()
async def disconnect(inter):
    global ssh
    ssh.close()
    try:
        ssh.exec_command('ls')
        await inter.response.send_message(x+"Something went wrong !")
    except:
        await inter.response.send_message(s+"Successfully disconnected !")
        
@client.slash_command()
async def run(inter, command):
    global ssh
    try:
        if not command:
            await inter.response.send_message(x+"U must provide a command to run !")
        else:
            stdin, stdout, stderr = ssh.exec_command(str(command))
            output = stdout.read()
            try:
                if not output:
                    await inter.response.send_message(s+"**"+command+"** ran succesfully, but there was no output.")
                else:
                    await inter.response.send_message(s+"**"+command+"** ran succesfully, theres the output !```"+output.decode("utf-8")+"```")
            except:
                await inter.response.send_message(x+"**"+command+"** does not exist or failed !")
    except:
        await inter.response.send_message(x+"Connection not available, please reconnect !")



client.run(token)