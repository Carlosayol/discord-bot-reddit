import praw
import discord
import os
import random

client = discord.Client()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
)

tech_subs = ["technology", "MachineLearning", "programming", "Python"]
news_subs = ["todayilearned", "worldnews", "TechNewsToday"]
ent_subs = ["Games", "Steam", "GameDeals"]
dict_subs = {"#tech": tech_subs, "#news": news_subs, "#ent": ent_subs, "#random": "all"}


def get_posts(subs):
    if subs == "all":
        post = random.choice([post for post in reddit.subreddit("all").hot(limit=20)])
    else:
        post = random.choice(
            [post for post in reddit.subreddit("+".join(subs)).hot(limit=15)]
        )
    return post.title, post.score, post.url, post.subreddit.display_name


def makeEmbed(t, s, u, n):
    embedTem = discord.Embed(title=n, description=t, color=0x00ADB5)
    embedTem.add_field(name="Score", value=s, inline=True)
    embedTem.add_field(name="URL", value=f"[URL]({u})", inline=True)
    return embedTem


@client.event
async def on_ready():
    print("Working")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith(("#tech", "#news", "#ent", "#random")):
        title, score, url, name = get_posts(dict_subs[msg])
        embedTab = makeEmbed(title, score, url, name)
        await message.channel.send(embed=embedTab)


client.run(os.getenv("TOKEN"))
