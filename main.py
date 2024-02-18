import discord
import asyncio
import time
import json
import os
from discord.ext import commands
from pystyle import Colors, Colorate

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            message_content = input((Colorate.Color(Colors.blue, "Enter the message to send to all members or type 'config' to use config.json : ")))

            if "config" in message_content.lower():
                with open('config.json', 'r') as config_file:
                    config_data = json.load(config_file)

                embed = discord.Embed(
                    title=config_data["dm_config"]["title"],
                    description=config_data["dm_config"]["description"],
                    color=config_data["dm_config"]["color"]
                )

                embed.set_thumbnail(url=config_data["dm_config"]["thumbnail"])

                for field in config_data["dm_config"]["fields"]:
                    embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])

                embed.set_footer(text=config_data["dm_config"]["footer"]["text"], icon_url=config_data["dm_config"]["footer"]["icon_url"])

                cooldown_embed = await asyncio.to_thread(lambda: float(input((Colorate.Color(Colors.blue, "Enter the cooldown duration for embeds (seconds): ")))))

                for member in guild.members:
                    if not member.bot:
                        try:
                            start_time_member = time.time()
                            await member.send(embed=embed)
                            end_time_member = time.time()
                            print((Colorate.Color(Colors.green, f"[+] Embed Sent to {member.name} ({member.id}) - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                            await asyncio.sleep(cooldown_embed)
                        except Exception as e:
                            print((Colorate.Color(Colors.red, f"[-] Can't send embed to {member.name}: {e}")))
            else:
                members_sent = 0
                members_fail = 0

                cooldown_message = await asyncio.to_thread(lambda: float(input((Colorate.Color(Colors.blue, "Enter the cooldown duration for messages (seconds): ")))))

                start_time_total = time.time()  
                for member in guild.members:
                    if not member.bot:
                        try:
                            start_time_member = time.time() 
                            await member.send(message_content)
                            end_time_member = time.time() 
                            print((Colorate.Color(Colors.green, f"[+] Message Sent to {member.name} ({member.id}) - Time taken: {end_time_member - start_time_member:.2f} seconds")))
                            members_sent += 1

                            await asyncio.sleep(cooldown_message)

                        except Exception as e:
                            print((Colorate.Color(Colors.red, f"[-] Can't send message to {member.name}: {e}")))
                            members_fail += 1

                end_time_total = time.time()  
                print((Colorate.Color(Colors.blue, f"[!] Command Used: DM All - {members_sent} messages sent, {members_fail} messages failed - Total Time taken: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Color(Colors.red, "[-] Guild not found.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Error: {e}")))


bot_token = input((Colorate.Color(Colors.blue, "Enter Bot Token: ")))
server_id = input((Colorate.Color(Colors.blue, "Enter Server ID: ")))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print((Colorate.Color(Colors.blue, f'[+] {bot.user.name} is online!')))
    print((Colorate.Color(Colors.blue, f'[+] Server ID: {server_id}')))

    server = bot.get_guild(int(server_id))
    if server:
        print((Colorate.Color(Colors.green, f'[+] Bot is in the specified server ({server.name})')))
        

    else:
        print((Colorate.Color(Colors.red, f'[-] Bot is not in the specified server')))
        return
    

    time.sleep(2)


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input((Colorate.Color(Colors.blue, """
        ·▄▄▄▄  • ▌ ▄ ·.      ▄▄▄· ▄▄▌  ▄▄▌      ▄▄▄▄·       ▄▄▄▄▄
        ██▪ ██ ·██ ▐███▪    ▐█ ▀█ ██•  ██•      ▐█ ▀█▪▪     •██  
        ▐█· ▐█▌▐█ ▌▐▌▐█·    ▄█▀▀█ ██▪  ██▪      ▐█▀▀█▄ ▄█▀▄  ▐█.▪
        ██. ██ ██ ██▌▐█▌    ▐█ ▪▐▌▐█▌▐▌▐█▌▐▌    ██▄▪▐█▐█▌.▐▌ ▐█▌·
        ▀▀▀▀▀• ▀▀  █▪▀▀▀     ▀  ▀ .▀▀▀ .▀▀▀     ·▀▀▀▀  ▀█▄▀▪ ▀▀▀ 
                        
                            1. Dm All Server
                            2. Exit
        Choice : """)))

        if choice == '1':
            await dm_all(server_id)

        elif choice == '2':
            print((Colorate.Color(Colors.blue, "Exiting the bot")))
            break

        else:
            print((Colorate.Color(Colors.red, "Invalid choice. Please enter a valid option.")))

        await asyncio.sleep(3)

if __name__ == "__main__":
    bot.run(bot_token)
