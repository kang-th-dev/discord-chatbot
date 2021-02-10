import discord
from discord.ext import commands
import json
from module import crawling

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as `',client.user.id,'`')
    print('-------------------------')

@client.event
async def on_member_join(member):
    print(member + " join")
    await member.send(str(member)+" 님 환영합니다!!")

@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
        await message.channel.send('pong')

    if message.content.startswith("#날씨"):
        getWeather = crawling.getWeatherInfo(message.content[4:])
        if getWeather == "none":
            await message.channel.send(embed=discord.Embed(title="not found", description="지역을 조금 더 정확하게 표기해주세요", color=0x62c1cc))
        else:
            await message.channel.send(embed=discord.Embed(title=getWeather["temperature"], description=getWeather["location"], color=0x62c1cc))

    if message.content.startswith("#미세먼지"):
        getAirInfor = crawling.getAirpollution(message.content[6:])
        if getAirInfor == "none":
            await message.channel.send(embed=discord.Embed(title="not found", description="지역을 조금 더 정확하게 표기해주세요", color=0x62c1cc))
        else:
            await message.channel.send(embed=discord.Embed(title=getAirInfor["airPollution"], description=getAirInfor["location"], color=0x62c1cc))

    if message.content.startswith("#뉴스"):
        newsList = crawling.getNews(message.content[4:])
        if newsList == "none":
            embed = discord.Embed(title="[ News Command Help ]"  ,  color=0x6233cc)
            embed.add_field(name= "Topic type", value="사회, 정치, 경제, 국제, 문화, IT", inline=False)
            embed.add_field(name= "How to use", value="#뉴스 [title]", inline=False)
        else:
            embed = discord.Embed(title=message.content[4:]+" News Topic" , description="list", color=0x6233cc)
            newsHeadLine = list(newsList.keys())
            for i in range(len(newsHeadLine)):
                embed.add_field(name= newsHeadLine[i], value=newsList[newsHeadLine[i]], inline=False)

        await message.channel.send(embed=embed)
    
    if message.content.startswith("#채널생성"):
        channel_name = message.content[6:]
        
        await message.guild.create_text_channel(str(channel_name))


with open('./token.json','r') as f:
    client.run(json.load(f)["data"])