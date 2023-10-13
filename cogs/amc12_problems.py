from discord.ext import commands
from discord.ext.commands import Context
import requests
import discord
import random
from discord import Button, ButtonStyle

amc10_id = ["10A", "10B"]
amc12_id = ["12A", "12B"]
amc_id = ["10A", "10B", "12A", "12B"]
aime_id = ["1", "2"]

class Choice(discord.ui.View):
    value = None
    clicked: bool = False
    timeout = 10000

    def __init__(self, sol, randomyear, amc10_contestid, amc_medium, right_response_embed, wrong_response_embed,
                 author):
        self.sol = sol
        self.randomyear = randomyear
        self.amc10_contestid = amc10_contestid
        self.amc_medium = amc_medium
        self.right_response_embed = right_response_embed
        self.wrong_response_embed = wrong_response_embed
        self.author = author
        super().__init__()

    async def disable_all_items(self):
        for item in self.children:
            
            item.disabled = True

    async def disable_if_clicked(self):
        if self.clicked:
            await self.disable_all_items()
        
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        # await self.message.channel.send("Timed out due to inactivity. You may want to donate some money to cover server costs.")
        await self.disable_all_items()

    async def boiler_plate(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            if self.value == str(self.sol):
                await interaction.response.send_message(embed=self.right_response_embed)
            else:
                await interaction.response.send_message(embed=self.wrong_response_embed)
            self.clicked = True
            await self.disable_all_items()
        else:
            await interaction.response.send_message(f"You are not the author of this message {interaction.user.mention}")
            self.clicked = False
        self.clicked = True
        await self.disable_if_clicked()
        self.stop()

    @discord.ui.button(label="A", style=discord.ButtonStyle.blurple)
    async def choiceA(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "a"
        await self.boiler_plate(interaction)

    @discord.ui.button(label="B", style=discord.ButtonStyle.blurple)
    async def choiceB(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "b"
        await self.boiler_plate(interaction)

    @discord.ui.button(label="C", style=discord.ButtonStyle.blurple)
    async def choiceC(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "c"
        await self.boiler_plate(interaction)

    @discord.ui.button(label="D", style=discord.ButtonStyle.blurple)
    async def choiceD(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "d"
        await self.boiler_plate(interaction)

    @discord.ui.button(label="E", style=discord.ButtonStyle.blurple)
    async def choiceE(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "e"
        await self.boiler_plate(interaction)
    
    
    @discord.ui.button(label="DM Solution", style=discord.ButtonStyle.danger)
    async def choiceF(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id == self.author.id:
            await interaction.response.send_message(f"You asked for the question. I cannot DM you the answer. {interaction.user.mention}")
            return
        user = interaction.user
        try:
            await user.send(f"The solution is {self.sol}")
        except discord.errors.Forbidden:
            await interaction.response.send_message("I am unable to send you a DM. Please check your privacy settings.")
        else:
            await interaction.response.send_message(f"DM sent to {user.mention}")
        finally:
            self.clicked = False
            await interaction.response.defer()
            self.stop()

    @discord.ui.button(label="AoPS Link", style=discord.ButtonStyle.danger)
    async def choiceG(self, interaction: discord.Interaction, button: discord.ui.Button):
        url = f"https://artofproblemsolving.com/wiki/index.php?title={self.randomyear}_AMC_{self.amc10_contestid}_Problems/Problem_{self.amc_medium}"
        if interaction.user.id == self.author.id:
            await interaction.response.send_message(f"Please complete question first {interaction.user.mention}")
            self.clicked = False
        else:
            await interaction.response.send_message(f"AoPS Link: {url}")
            self.clicked = True
            await self.disable_if_clicked()
            self.stop()
            
        


class AMC12(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # displays ready message on load
    @commands.Cog.listener()
    async def on_ready(self):
        print("AMC12 cog has been loaded sucessfully")

    @commands.command()
    async def amc12(self, ctx, difficulty):
        
        user_guild_id = ctx.guild.id
        author = ctx.author.id
        author = ctx.author

        status_color = {"easy": 0x3CB371, "medium": 0xFF8C00, "hard": 0xED1C24}
        tried = []

        if difficulty.lower() == "e" or difficulty.lower() == "easy":
            randomyear = str(random.randint(2002, 2019))
            amc_easy = str(random.randint(1, 10))
            amc12_contestid = str(random.choice(amc12_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc12_contestid} Problem {amc_easy} invoked by {author.name}",
                color=status_color["easy"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_easy}/statement.png"
            )
            question_embed.set_footer(text=f"@{author.name}")
            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_easy}/sol.txt"
                    ).text
                ).strip()
            )
            right_response_embed = discord.Embed(description = (
                    f"Correct Answer `{sol.upper()}`. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_easy})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_easy})"
                    ))
            # essential_arguements= essential_arguements(sol=sol, randomyear=randomyear, amc12_contestid=amc12_contestid, amc_easy=amc_easy)
            
            buttons= Choice(sol, randomyear, amc12_contestid, amc_easy, right_response_embed, wrong_response_embed, author)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")
            

        if difficulty.lower() == "m" or difficulty.lower() == "medium":
            randomyear = str(random.randint(2002, 2019))
            amc_medium = str(random.randint(11, 16))
            amc12_contestid = str(random.choice(amc12_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc12_contestid} Problem {amc_medium} invoked by @{ctx.author.name}",
                color=status_color["medium"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_medium}/statement.png"
            )

            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_medium}/sol.txt"
                    ).text
                ).strip()
            )
            
            right_response_embed = discord.Embed(description = (
                    f"Correct Answer `{sol.upper()}`. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_medium})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_medium})"
                    ))
            
            buttons= Choice(sol, randomyear, amc12_contestid, amc_medium, right_response_embed, wrong_response_embed, author)
            print(sol)
            question = await ctx.send(ctx.message.author.mention ,embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")


        if difficulty.lower() == "h" or difficulty.lower() == "hard":
            randomyear = str(random.randint(2002, 2019))
            amc_hard = str(random.randint(17, 25))
            amc12_contestid = str(random.choice(amc12_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc12_contestid} Problem {amc_hard} invoked by {ctx.author.name}",
                color=status_color["hard"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_hard}/statement.png"
            )

            question_embed.set_footer(text=f"Click on the button to submit your answer {author.mention}")
            
            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc12_contestid}/{amc_hard}/sol.txt"
                    ).text
                ).strip()
            )

            right_response_embed = discord.Embed(description = ( f"Correct Answer. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_hard})"))
            wrong_response_embed = discord.Embed(description = ( f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc12_contestid}_Problems/Problem_{amc_hard})"))
            buttons= Choice(sol, randomyear, amc12_contestid, amc_hard, right_response_embed, wrong_response_embed, author)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")

async def setup(bot):
    await bot.add_cog(AMC12(bot))
