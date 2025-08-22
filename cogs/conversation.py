from discord.ext import commands
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

system_prompt = "Dein Name ist 'Conan'. Du bist ein Discord Bot und sollst dich wie Detectiv Conan verhalten und so auch schreiben, nur dass du nicht wirklich Verbrechen löst. Du bist einfach so smart wie Detekitv Conan, du sollst nicht jedes mal einen grüßen und auch nicht dauernd erzählen, dass du keine Verbrechen suchst"

history = [{"role": "system", "content": system_prompt}]



def gpt4(prompt):
    history.append({"role": "user", "content": prompt})

    messages_to_send = [history[0]] + history[-(10 * 2):]

    response = client.chat.completions.create(
        model="gpt-5-nano",
        max_completion_tokens=10000,
        temperature=1,
        messages=messages_to_send
    )

    try:
        assistant_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as error:
        print(error)
        return


class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(f'<@{self.bot.user.id}>') or message.content.startswith(f'<@!{self.bot.user.id}>'):
            user = message.author
            message_dc = f"{user}: {message.content}"

            result = gpt4(message_dc)
            await message.channel.send(f"{user.mention} {result}")


def setup(bot):
    bot.add_cog(Ai(bot))