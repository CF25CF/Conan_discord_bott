import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="test", description="Testet ob der Bot funktioniert")
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("✅ Test erfolgreich! Conan ist bereit.")
    
    @discord.slash_command(name="embed", description="Zeigt ein maximales Discord Embed mit allen Features")
    async def embed(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="🚀 **MAXIMALES DISCORD EMBED MIT ALLEN FEATURES** 🚀",
            url="https://discord.com",
            description="## 📋 **Komplette Embed-Demo mit allen Möglichkeiten**\n"
                        "═══════════════════════════════════════\n\n"
                        "### 🎨 **Text-Formatierung:**\n"
                        "• **Fett** • *Kursiv* • ***Fett & Kursiv***\n"
                        "• ~~Durchgestrichen~~ • __Unterstrichen__ • __*Unterstrichen Kursiv*__\n"
                        "• `Inline Code` • ||Spoiler Text||\n\n"
                        "### 📝 **Code-Blöcke mit Syntax-Highlighting:**\n"
                        "```python\n"
                        "# Python Code\n"
                        "def discord_embed():\n"
                        "    return 'Awesome!'\n"
                        "```\n"
                        "```javascript\n"
                        "// JavaScript Code\n"
                        "const embed = new Discord.MessageEmbed();\n"
                        "```\n\n"
                        "### 🔗 **Links & Erwähnungen:**\n"
                        "• [🔗 Klickbarer Link zu Discord](https://discord.com)\n"
                        "• [📚 GitHub Repository](https://github.com)\n"
                        "• Erwähnung: <@123456789> (User)\n"
                        "• Channel: <#123456789> (Channel)\n"
                        "• Rolle: <@&123456789> (Role)\n\n"
                        "### 💬 **Zitat-Blöcke:**\n"
                        "> Dies ist ein einfaches Zitat\n"
                        "> Mit mehreren Zeilen\n\n"
                        ">>> Dies ist ein mehrzeiliger\n"
                        "Block-Zitat der alles\n"
                        "einschließt bis zum Ende\n\n"
                        "### 📊 **Listen & Aufzählungen:**\n"
                        "1️⃣ Erste numerierte Option\n"
                        "2️⃣ Zweite numerierte Option\n"
                        "3️⃣ Dritte numerierte Option\n\n"
                        "✅ Checkbox-Style\n"
                        "❌ Nicht erfüllt\n"
                        "⚠️ Warnung\n"
                        "📌 Wichtig\n\n"
                        "### 🌈 **Emojis & Symbole:**\n"
                        "😀 😃 😄 😁 😆 😅 🤣 😂 🙂 🙃\n"
                        "🔥 💯 ⭐ 🎉 🎊 🎈 🎁 🏆 🥇 🏅\n"
                        "⚡ 💎 💰 🚀 🛸 🌟 ✨ 💫 🌙 ☀️",
            color=discord.Color.from_rgb(255, 0, 255)
        )
        
        embed.set_author(
            name="⭐ Premium Autor mit Avatar und Link",
            url="https://github.com",
            icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
        )
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png")
        
        embed.set_image(url="https://picsum.photos/800/400")
        
        embed.add_field(
            name="📊 **Statistiken**",
            value="```diff\n"
                  "+ 95% Erfolgsrate\n"
                  "- 5% Fehlerquote\n"
                  "! 1000 Aktive User\n"
                  "# Server: Online\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="🎮 **Gaming Stats**",
            value="```yaml\n"
                  "Level: 99\n"
                  "XP: 999,999\n"
                  "Rang: Legendär\n"
                  "K/D: 5.43\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="📈 **System Performance**",
            value="```css\n"
                  "[CPU: 45%]\n"
                  "[RAM: 2.5GB/8GB]\n"
                  "[Ping: 12ms]\n"
                  "[Uptime: 99.9%]\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="🌍 **Sprachen**",
            value="```ini\n"
                  "[Deutsch] = Aktiv\n"
                  "[English] = Active\n"
                  "[Español] = Activo\n"
                  "[日本語] = アクティブ\n"
                  "```",
            inline=True
        )
        

        
        embed.add_field(
            name="🔢 **Fortschrittsbalken**",
            value="```\n"
                  "Download: [████████░░] 80%\n"
                  "Upload:   [██████░░░░] 60%\n"
                  "Process:  [██████████] 100%\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="\u200b",
            inline=False
        )
        
        embed.add_field(
            name="🎨 **ASCII Art & Boxen**",
            value="```\n"
                  "╔═══════════════════╗\n"
                  "║   DISCORD EMBED   ║\n"
                  "║   MAX FEATURES    ║\n"
                  "╚═══════════════════╝\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="🌈 **ANSI Farben**",
            value="```ansi\n"
                  "\u001b[31mRot\u001b[0m \u001b[32mGrün\u001b[0m \u001b[34mBlau\u001b[0m\n"
                  "\u001b[33mGelb\u001b[0m \u001b[35mMagenta\u001b[0m \u001b[36mCyan\u001b[0m\n"
                  "\u001b[41mHintergrund\u001b[0m\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="📋 **Tabelle**",
            value="```\n"
                  "┌─────┬──────┬─────┐\n"
                  "│ ID  │ Name │Score│\n"
                  "├─────┼──────┼─────┤\n"
                  "│ 001 │ Max  │ 100 │\n"
                  "│ 002 │ Anna │  95 │\n"
                  "└─────┴──────┴─────┘\n"
                  "```",
            inline=True
        )
        
        embed.add_field(
            name="🔗 **Social Media Links**",
            value="[Twitter](https://twitter.com) | "
                  "[YouTube](https://youtube.com) | "
                  "[GitHub](https://github.com) | "
                  "[Discord](https://discord.com)",
            inline=False
        )
        
        embed.add_field(
            name="📝 **Discord Embed Limits**",
            value="• **Title:** 256 Zeichen\n"
                  "• **Description:** 4096 Zeichen\n"
                  "• **Fields:** 25 Maximum\n"
                  "• **Field Name:** 256 Zeichen\n"
                  "• **Field Value:** 1024 Zeichen\n"
                  "• **Footer:** 2048 Zeichen\n"
                  "• **Author:** 256 Zeichen\n"
                  "• **Gesamt:** 6000 Zeichen",
            inline=False
        )
        
        embed.set_footer(
            text="📌 Footer mit Icon | Powered by Discord.py | © 2024 Conan Bot | Alle Features demonstriert",
            icon_url="https://cdn.discordapp.com/embed/avatars/2.png"
        )
        

        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Test(bot))