from discord.ext import commands

import requests
import discord
import random


amc10_id = ["10A", "10B"]
amc12_id = ["12A", "12B"]
amc_id = ["10A", "10B", "12A", "12B"]
aime_id = ["1", "2"]


class Choice(discord.ui.View):
    value = None
    clicked:bool = False
    timeout=1000
    
    def __init__(self, sol, randomyear, amc10_contestid, amc_medium, right_response_embed, wrong_response_embed):
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

class ContestProblems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # displays ready message on load
    @commands.Cog.listener()
    async def on_ready(self):
        print("Contest problems cog has been loaded sucessfully")

    @commands.command(name="cmo", description="Displays a random CMO problem")
    async def cmo(self, ctx):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id

        cmo_year = random.randint(1969, 1973)
        cmo_question = random.randint(1, 9)
        requested_path = f"CMO/{cmo_year}/{cmo_question}"

        question_embed = discord.Embed(
            title=f"{cmo_year} CMO Problem {cmo_question}",
            description=f"<@{ctx.author.id}> Bot is still in alpha, Solution may be available soon.",
            color=0xCF9FFF,
        ).set_image(
            url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/{requested_path}/statement.png"
        )

        await ctx.send(embed=question_embed)

    @commands.command(name="aime")
    async def aime(self, ctx):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id
        
        aime_year = random.randint(1983, 2019)
        aime_version = random.randint(1, 2)
        aime_question = random.randint(1, 15)
        requested_path = ""

        question_embed = discord.Embed(
            description=f"<@{ctx.author.id}> Bot is still in development, solution will be available soon..",
            color=0xCF9FFF,
        )

        if aime_year < 2000:
            requested_path = f"AIME/{aime_year}/{aime_question}"
            question_embed.title = f"{aime_year} AIME Problem {aime_question}"
        else:
            requested_path = f"AIME/{aime_year}/{aime_version}/{aime_question}"
            question_embed.title = (
                f"{aime_year} AIME {'I'*aime_version} Problem {aime_question}"
            )

        question_embed.set_image(
            url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/{requested_path}/statement.png"
        )

        await ctx.send(embed=question_embed)

    @commands.command()
    async def fetch(self, ctx, *, args=None):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id
        
        if args is not None:
            contest_data = args.upper().split()
            requested_path = args.upper().replace(" ", "/")
            tried = []
            question_embed = discord.Embed(
                title=f"{contest_data[1]} {contest_data[0]} {' '.join(contest_data[2:-1])+' '}Problem {contest_data[-1]}",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/{requested_path}/statement.png"
            )

            

            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/{requested_path}/sol.txt"
                    ).text
                ).strip()
            )

            buttons= Choice(sol, None, None, None, None, None)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")

    @commands.command(aliases=["l5", "last5", "lfive"])
    async def lastfive(self, ctx, args):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id
        

        def parse_args(args):
            if "aime" in args.lower():
                return "aime"
            elif "usamo" in args.lower():
                return "usamo"
            elif "usajmo" in args.lower():
                return "usajmo"
            elif args.lower() == "amc10":
                return "amc10"
            elif args.lower() == "amc12":
                return "amc12"

        parsed_arg = parse_args(args)

        tried = []

        if parsed_arg == "aime":
            random_aime_id = random.choice(aime_id)
            aime_year = str(random.randint(2000, 2019))
            last_5 = str(random.randint(10, 15))

            question_embed = discord.Embed(
                title=f"{aime_year} AIME {'I'*random_aime_id} Problem {last_5}",
                description=f"<@{ctx.author.id}> Bot is still in development, solution will be available soon..",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AIME/{aime_year}/{random_aime_id}/{last_5}/statement.png"
            )
            await ctx.send(embed=question_embed)

        elif parsed_arg == "usamo":
            usamo_year = str(random.randint(1972, 2019))
            last_5 = str(random.randint(1, 5))

            question_embed = discord.Embed(
                title=f"{usamo_year} USAMO Problem {last_5}",
                description=f"<@{ctx.author.id}> Bot is still in development, solution will be available soon..",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/USAJMO/{usamo_year}/{last_5}/statement.png"
            )
            await ctx.channel.send(embed=question_embed)
        elif parsed_arg == "usajmo":
            usajmo_year = str(random.randint(2010, 2019))
            last_5 = str(random.randint(1, 5))

            question_embed = discord.Embed(
                title=f"{usajmo_year} USAJMO Problem {last_5}",
                description=f"<@{ctx.author.id}> Bot is still in development, solution will be available soon..",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/USAJMO/{usajmo_year}/{last_5}/statement.png"
            )

            await ctx.channel.send(embed=question_embed)
        elif parsed_arg == "amc10":
            random_year = str(random.randint(2002, 2019))
            last_5 = str(random.randint(20, 25))
            amc_id = str(random.choice(amc10_id))

            question_embed = discord.Embed(
                title=f"{random_year} AMC {amc_id} Problem {last_5}",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{amc_id}/{last_5}/statement.png"
            )

            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{amc_id}/{last_5}/sol.txt"
                    ).text
                ).strip()
            )

            right_response_embed = discord.Embed(description = (
                    f"Correct Answer. Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_year}_AMC_{amc_id}_Problems/Problem_{last_5})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_year}_AMC_{amc_id}_Problems/Problem_{last_5})."
                    ))

            buttons= Choice(sol, random_year, amc_id, last_5, right_response_embed, wrong_response_embed)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")

        elif parsed_arg == "amc12":
            random_year = str(random.randint(2002, 2019))
            last_5 = str(random.randint(20, 25))
            amc_id = str(random.choice(amc12_id))

            question_embed = discord.Embed(
                title=f"{random_year} AMC {amc_id} Problem {last_5}",
                color=0xCF9FFF,
            ).set_image(
                url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{amc_id}/{last_5}/statement.png"
            )

            

            sol = str(
                (
                    requests.get(
                        f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{amc_id}/{last_5}/sol.txt"
                    ).text
                ).strip()
            )

            right_response_embed = discord.Embed(description = (
                    f"Correct Answer. Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_year}_AMC_{amc_id}_Problems/Problem_{last_5})"
                    ))
            wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_year}_AMC_{amc_id}_Problems/Problem_{last_5})."
                    ))

            buttons= Choice(sol, random_year, amc_id, last_5, right_response_embed, wrong_response_embed)
            print(sol)
            question = await ctx.send(embed=question_embed, view=buttons)
            buttons.message = question
            await buttons.wait()
            print(f"value of button is {buttons.value}")


    @commands.command(aliases=["rnd"])
    async def random(self, ctx):
        user_guild_id = ctx.guild.id
        user_id = ctx.author.id
        
        tried = []
        random_contest = str(random.choice(amc_id))
        random_year = str(random.randint(2002, 2019))
        random_problem = str(random.randint(1, 25))

        question_embed = discord.Embed(
            title=f"{random_year} AMC {random_contest} Problem {random_problem}",
            color=0x00BFFF,
        ).set_image(
            url=f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{random_contest}/{random_problem}/statement.png"
        )

        

        sol = str(
            (
                requests.get(
                    f"https://raw.githubusercontent.com/yak-fumblepack/mathcontests/master/AMC/{random_year}/{random_contest}/{random_problem}/sol.txt"
                ).text
            ).strip()
        )

        right_response_embed = discord.Embed(description = (
                    f"Correct Answer. Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_year}_AMC_{random_contest}_Problems/Problem_{random_problem})"))

        wrong_response_embed = discord.Embed(description = (
                    f"Wrong Answer. Correct was `{sol.upper()}`. How? Solution is [here](https://artofproblemsolving.com/wiki/index.php?title={random_contest}_AMC_{amc_id}_Problems/Problem_{random_problem})."))

        buttons= Choice(sol, random_year, amc_id, random_problem, right_response_embed, wrong_response_embed)
        print(sol)
        question = await ctx.send(embed=question_embed, view=buttons)
        buttons.message = question
        await buttons.wait()
        print(f"value of button is {buttons.value}")
                

async def setup(bot):
    await bot.add_cog(ContestProblems(bot))
