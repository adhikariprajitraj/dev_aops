from discord.ext import commands

import requests
import discord
import random


questions_attempted_amount = 1
questions_failed_amount = 1
questions_solved_amount = 1

amc10_solved_amount = 1
amc12_solved_amount = 1
amc10_failed_amount = 1
amc12_failed_amount = 1

amc12_correct_amount_easy = 2
amc12_wrong_amount_easy = -4
amc12_correct_amount_med = 6
amc12_wrong_amount_med = -1.5
amc12_correct_amount_hard = 15
amc12_wrong_amount_hard = -0.5
amc12_attempted_amount = 1

amc10_correct_amount_easy = 2
amc10_wrong_amount_easy = -5  # push players to work for higher scores
amc10_correct_amount_med = 6
amc10_wrong_amount_med = -1.5
amc10_correct_amount_hard = 15
amc10_wrong_amount_hard = -0.5
amc10_attempted_amount = 1

aime_attempted_amount = 1
usamo_attempted_amount = 1
usajmo_attempted_amount = 1
cmo_attempted_amount = 1

amc12_weight = 0.65
amc10_weight = 0.35
amc10_id = ["10A", "10B"]
amc12_id = ["12A", "12B"]
amc_id = ["10A", "10B", "12A", "12B"]
aime_id = ["1", "2"]
reactions = {"🇦": "a", "🇧": "b", "🇨": "c", "🇩": "d", "🇪": "e", "❎": "quit"}


from discord import app_commands


class Choice(discord.ui.View):
    value = None
    clicked:bool = False
    timeout=1000
    
    def __init__(self,sol, randomyear, amc10_contestid, amc_medium, right_response_embed, wrong_response_embed):
        self.sol = sol
        self.randomyear = randomyear
        self.amc10_contestid = amc10_contestid
        self.amc_medium = amc_medium
        self.right_response_embed=  right_response_embed
        self.wrong_response_embed=  wrong_response_embed
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
    

    @discord.ui.button(label="A", style=discord.ButtonStyle.blurple)
    async def choiceA(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "a"
        if self.value == str(self.sol):
            await interaction.response.send_message(embed=self.right_response_embed)
        else:
            await interaction.response.send_message(embed=self.wrong_response_embed)
        self.clicked = True
        await self.disable_all_items()

        self.stop()

    @discord.ui.button(label="B", style=discord.ButtonStyle.blurple)
    async def choiceB(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "b"
        if self.value == str(self.sol):
            await interaction.response.send_message(embed=self.right_response_embed)
        else:
            await interaction.response.send_message(embed=self.wrong_response_embed)
        self.clicked = True
        await self.disable_if_clicked()
        self.stop()

    @discord.ui.button(label="C", style=discord.ButtonStyle.blurple)
    async def choiceC(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "c"
        if self.value == str(self.sol):
            await interaction.response.send_message(embed=self.right_response_embed)
        else:
            await interaction.response.send_message(embed=self.wrong_response_embed)
        self.clicked = True
        await self.disable_if_clicked()
        self.stop()
    
    @discord.ui.button(label="D", style=discord.ButtonStyle.blurple)
    async def choiceD(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "d"
        if self.value == str(self.sol):
            await interaction.response.send_message(embed=self.right_response_embed)
        else:
            await interaction.response.send_message(embed=self.wrong_response_embed)
        self.clicked = True
        await self.disable_if_clicked()
        self.stop()
    
    @discord.ui.button(label="E", style=discord.ButtonStyle.blurple)
    async def choiceE(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "e"
        if self.value == str(self.sol):
            await interaction.response.send_message(embed=self.right_response_embed)
        else:
            await interaction.response.send_message(embed=self.wrong_response_embed)
        self.clicked = True
        await self.disable_if_clicked()
        self.stop()


class AMC10(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # displays ready message on load
    @commands.Cog.listener()
    async def on_ready(self):
        print("AMC10 cog has been loaded sucessfully")

    @commands.command()
    async def amc10(self, ctx, difficulty):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id
        
        status_color = {"easy": 0x3CB371, "medium": 0xFF8C00, "hard": 0xED1C24}


        if difficulty.lower() == "e" or difficulty.lower() == "easy":
            randomyear = str(random.randint(2002, 2019))
            amc_easy = str(random.randint(1, 10))
            amc10_contestid = str(random.choice(amc10_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc10_contestid} Problem {amc_easy}",
                color=status_color["easy"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_easy}/statement.png"
            )

            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_easy}/sol.txt"
                    ).text
                ).strip()
            )
            right_response_embed = discord.Embed(description = (
                    f"Correct Answer. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_easy})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_easy})"
                    ))
            # essential_arguements= essential_arguements(sol=sol, randomyear=randomyear, amc10_contestid=amc10_contestid, amc_easy=amc_easy)
            
            buttons= Choice(sol, randomyear, amc10_contestid, amc_easy, right_response_embed, wrong_response_embed)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")
                

        if difficulty.lower() == "m" or difficulty.lower() == "medium":
            randomyear = str(random.randint(2002, 2019))
            amc_medium = str(random.randint(11, 16))
            amc10_contestid = str(random.choice(amc10_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc10_contestid} Problem {amc_medium}",
                color=status_color["medium"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_medium}/statement.png"
            )



            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_medium}/sol.txt"
                    ).text
                ).strip()
            )
            
            right_response_embed = discord.Embed(description = (
                    f"Correct Answer. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_medium})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_medium})"
                    ))
            
            buttons= Choice(sol, randomyear, amc10_contestid, amc_medium, right_response_embed, wrong_response_embed)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")
                

        if difficulty.lower() == "h" or difficulty.lower() == "hard":
            randomyear = str(random.randint(2002, 2019))
            amc_hard = str(random.randint(17, 25))
            amc10_contestid = str(random.choice(amc10_id))

            question_embed = discord.Embed(
                title=f"{randomyear} AMC {amc10_contestid} Problem {amc_hard}",
                color=status_color["hard"],
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_hard}/statement.png"
            )


            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{randomyear}/{amc10_contestid}/{amc_hard}/sol.txt"
                    ).text
                ).strip()
            )

            right_response_embed = discord.Embed(description = ( f"Correct Answer. Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_hard})"))
            wrong_response_embed = discord.Embed(description = ( f"Wrong Answer. Correct was `{sol.upper()}`. How? Source of the problem is [here](https://artofproblemsolving.com/wiki/index.php?title={randomyear}_AMC_{amc10_contestid}_Problems/Problem_{amc_hard})"))
            buttons= Choice(sol, randomyear, amc10_contestid, amc_hard, right_response_embed, wrong_response_embed)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")

async def setup(bot):
    await bot.add_cog(AMC10(bot))
