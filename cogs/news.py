import os
import json
import requests
from openai import OpenAI
from datetime import timedelta
from discord.ext import commands, tasks
from datetime import datetime
import discord

# normale URL: https://www.tagesschau.de/wirtschaft/unternehmen/streik-amazon-verteilzentrum-100.html
# API URL: https://www.tagesschau.de/api2u/wirtschaft/unternehmen/streik-amazon-verteilzentrum-100.json

# ================== Konfiguration ==================
NEWS_CHANNEL_ID = os.getenv("NEWS_CHANNEL_ID")
TAGESSCHAU_API_URL = "https://www.tagesschau.de/api2u/news/"
WIRTSCHAFT_RESSORT = "wirtschaft"


OPENAI_API_KEY = os.getenv("OPEN_AI_KEY_2")
OPENAI_MODEL = "gpt-5"
openai_client = OpenAI(api_key=OPENAI_API_KEY)


NUMMER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


DAILY_NEWS_HOUR = 7
DAILY_NEWS_MINUTE = 59

# ================== Helper Funktionen ==================
def get_today_date():
    return datetime.now().date()

def get_yesterday_date():
    german_time = datetime.now()
    yesterday = german_time - timedelta(days=1)
    return yesterday.date()

def get_all_article(target_date, ressort):
    all_articles = []

    response = requests.get(
        TAGESSCHAU_API_URL,
        params={"ressort": ressort},
        timeout=15
    )
    response.raise_for_status()
    data = response.json()

    for news in data.get("news"):
        tagesschau_date_iso = news.get("date")
        tagesschau_date_datetime = datetime.fromisoformat(tagesschau_date_iso.replace("Z", "+00:00"))
        if target_date == tagesschau_date_datetime.date():
            all_articles.append({
                "title": news.get("title"),
                "first_sentence": news.get("firstSentence"),
                "api_link": news.get("details"),
                "link": news.get("detailsweb")
            })

    return all_articles

def select_top5_articles(articles):
    prompt = f"""
    Hier sind Wirtschaftsnachrichten. 
    Wähle die 5 wichtigsten und interessantesten aus.
    Antworte nur mit einem JSON-Array. Jedes Element soll haben: title, first_sentence, api_link, link.

    Nachrichten:
    {json.dumps(articles, ensure_ascii=False)}
    """

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Du bist ein Wirtschaftsjournalist. Antworte nur mit validem JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_answer = response.choices[0].message.content
    top5_articles = json.loads(ai_answer)

    return top5_articles

def get_article_content(api_url):

    response = requests.get(api_url, timeout=15)
    response.raise_for_status()
    article_data = response.json()

    content_blocks = article_data.get("content")

    paragraphs = []

    for block in content_blocks:
        if block.get("type") == "text":
            text = block.get("value").strip()
            if text:
                paragraphs.append(text)

    return paragraphs


def summarize_article(articles):
    prompt = f"""
    Erstelle für jeden Artikel eine kurze, prägnante Zusammenfassung in 3 Sätzen.
    Antworte mit einem JSON-Objekt mit dem Key "summary" und einem Array von Strings.

    Artikel:
    {json.dumps(articles, ensure_ascii=False)}
    """
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system",
             "content": "Du bist ein Wirtschaftsjournalist. Erstelle prägnante Zusammenfassungen."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_answer = response.choices[0].message.content
    result = json.loads(ai_answer)

    return result.get("summary")

def create_embed_field(index, article):
    title = article.get("title")
    summary = article.get("summary")
    link = article.get("link")

    if index < len(NUMMER_EMOJIS):
        emoji = NUMMER_EMOJIS[index]
    else:
        emoji = f"{index + 1}."

    field_name = f"{emoji} {title}"

    link_text = f"\n🔗 [Artikel lesen]({link})"

    max_length = 1024 - len(link_text)
    if len(summary) > max_length:
        summary = summary[:max_length - 1] + "…"

    field_value = f"{summary}{link_text}"

    return field_name, field_value

def news_embed(date, news):
    embed = discord.Embed(
        title=f"📰 Top-5 Wirtschaftsnachrichten vom {date.strftime('%d.%m.%Y')}",
        description="☕ Guten Morgen, hier sind die News von gestern",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Quelle: tagesschau.de | Zusammenfassungen von ChatGPT")

    for i, article in enumerate(news[:5]):
        field_name, field_value = create_embed_field(i, article)
        embed.add_field(name=field_name, value=field_value, inline=False)

    return embed

# ================== News Cog ==================
class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.daily_news.start()

    @discord.slash_command(
        name="news",
        description="Zeigt die Top-5 Wirtschaftsnachrichten von heute an"
    )
    async def news_command(self, ctx):
        await ctx.defer()

        today_date = get_today_date()

        all_articles = get_all_article(today_date, WIRTSCHAFT_RESSORT)

        top5_articles = select_top5_articles(all_articles)

        for article in top5_articles:
            content = get_article_content(article["api_link"])
            summary = summarize_article([content])
            article["summary"] = summary[0]

        embed = news_embed(get_today_date(), top5_articles)
        await ctx.followup.send(embed=embed)

    @tasks.loop(minutes=1)
    async def daily_news(self):
        now = datetime.now()

        if now.hour == DAILY_NEWS_HOUR and now.minute == DAILY_NEWS_MINUTE:
            channel = self.bot.get_channel(int(NEWS_CHANNEL_ID))
            date_yesterday = get_yesterday_date()

            all_articles = get_all_article(date_yesterday, WIRTSCHAFT_RESSORT)

            top5_articles = select_top5_articles(all_articles)

            for article in top5_articles:
                content = get_article_content(article["api_link"])
                summary = summarize_article([content])
                article["summary"] = summary[0]

            embed = news_embed(get_yesterday_date(), top5_articles)
            await channel.send(embed=embed)

# ================== Setup Funktion ==================
def setup(bot):
    bot.add_cog(NewsCog(bot))
