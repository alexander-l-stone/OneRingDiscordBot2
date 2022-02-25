from discord.ext import commands
from discord import Embed
from random import randint

class OneRingCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def get_skill_roll(self, num_dice: int):
        die_array = []
        for i in range(0, num_dice):
            die_array.append(randint(1, 6))
        return die_array

    def get_weary_roll(self, num_dice: int):
        die_array = []
        for i in range(0, num_dice):
            d6 = randint(1, 6)
            if d6 < 4:
                d6 *= -1
            die_array.append(d6)
        return die_array
    
    def get_player_feat_roll(self, favored: int):
        """
            Rolls a feat die. If favored is < 1, this roll is unfavored.
            If favored is > 1, roll is favored.
            Returns a "bad" symbol as negative
        """
        original_roll = randint(1, 12)
        if original_roll == 11:
            original_roll *= -1
        if favored != 0:
            second_roll = randint(1, 12)
            if second_roll == 11:
                second_roll *= -1
        if favored > 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return (max(original_roll, second_roll), min(original_roll, second_roll)) 
        if favored < 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return (min(original_roll, second_roll), max(original_roll, second_roll)) 
        return (original_roll)
    
    def get_gm_feat_roll(self, favored: int):
        """
            Rolls a feat die. If favored is < 1, this roll is unfavored.
            If favored is > 1, roll is favored.
            Returns a "bad" symbol as negative
        """
        original_roll = randint(1, 12)
        if original_roll == 12:
            original_roll *= -1
        if favored != 0:
            second_roll = randint(1, 12)
            if second_roll == 12:
                second_roll *= -1
        if favored > 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return (max(original_roll, second_roll), min(original_roll, second_roll)) 
        if favored < 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return (min(original_roll, second_roll), max(original_roll, second_roll)) 
        return (original_roll)

    def generate_player_text_box(self, skill_roll:str, feat_roll:tuple(int,int)):
        rollData = self.parse_roll(skill_roll, feat_roll)
        embed = Embed(title=f"Total: {rollData[0]}", description=f"{rollData[1]}", colur=0xFF0000)
        if rollData[3] > 0:
            embed.add_field(name='Automatic Success', value='You rolled a Gandalf Rune', inline=False)
        embed.add_field(name='Number of Sixes', value=f"{rollData[2]}", inline=False)
        return embed
    
    def generate_gm_text_box(self, skill_roll:str, feat_roll:tuple(int,int)):
        rollData = self.parse_roll(skill_roll, feat_roll)
        embed = Embed(title=f"Total: {rollData[0]}", description=f"{rollData[1]}", colur=0xFF0000)
        if rollData[3] < 0:
            embed.add_field(name='Automatic Success', value='You rolled an Eye of Sauron', inline=False)
        embed.add_field(name='Number of Sixes', value=f"{rollData[2]}", inline=False)
        return embed

    def parse_text(self, text: str):
        text_array = text.split(' ')
        commands = {'favored': 0, 'weary': False, 'num_dice': 0}
        print(text_array)
        for text in text_array:
            if text == 'favored' or text == 'f' or text == 'F':
                commands['favored'] += 1
            elif text == 'unfavored' or text == 'u' or text == 'U':
                commands['favored'] -= 1
            elif text == 'weary' or text == 'w' or text == 'W':
                commands['weary'] = True
            elif text.isnumeric():
                commands['num_dice'] += int(text)
            else:
                commands['label'] += f"{commands['label']}{text} "
            print(commands)
        return commands

    def parse_roll(self, skill_roll, feat_roll):
        """
        Turns a roll into data to be displayed.
        returns (total, roll_string, num_sixes, specialFeat)
        """
        total = 0
        num_sixes = 0
        roll_string = ""
        for num in skill_roll:
            if num > 0:
                total += num
                if num == 6:
                    # underline sixes
                    roll_string = f"{roll_string}__{num}__ "
                else:
                    # normal value
                    roll_string = f"{roll_string}{num} "
            else:
                # display lost dice from weary crossed out
                num *= -1
                roll_string = f"{roll_string}~~{num}~~ "
            if num == 6:
                num_sixes += 1

        # feat die
        roll_string = f"{roll_string}| "

        if feat_roll[0] > 0:
            total += feat_roll[0]
            if feat_roll[0] == 12 or feat_roll[0] == 11:
                # bold special symbol
                roll_string = f"{roll_string}**{feat_roll[0]}** "
            else:
                # normal feat die
                roll_string = f"{roll_string}{feat_roll[0]} "
        else:
            # bad rune is crossed out and bold
            badFeat = -1*feat_roll[0]
            roll_string = f"{roll_string}~~**{badFeat}**~~ "
                
        # Ignored die, if any
        if len(feat_roll) > 1:
            ignoredFeat = feat_roll[1]
            if ignoredFeat < 0:
                ignoredFeat *= -1
            if ignoredFeat == 11 or ignoredFeat == 12:
                # cross out and bold ignored special symbol
                roll_string = f"{roll_string}~~**{-1*ignoredFeat}**~~ "
            else:
                # cross out ignored feat die
                roll_string = f"{roll_string}~~{-1*ignoredFeat}~~ "
        
        specialFeat = 0
        if abs(feat_roll[0]) == 11:
            specialFeat = -1
        elif abs(feat_roll[0]) == 12:
            specialFeat = 1

        return (total, roll_string, num_sixes, specialFeat)



    @commands.command(name="roll")
    async def roll(self, ctx: commands.Context, *, text: str):
        """
            Make a normal roll
        """
        parsed_commands = self.parse_text(text)
        if parsed_commands['weary']:
            skill_roll = self.get_weary_roll(parsed_commands['num_dice'])
        else:
            skill_roll = self.get_skill_roll(parsed_commands['num_dice'])
        feat_roll = self.get_player_feat_roll(parsed_commands['favored'])
        await ctx.send(embed=self.generate_player_text_box(skill_roll, feat_roll))
    
    @commands.command(name="gmroll")
    async def gmroll(self, ctx: commands.Context, *, text: str):
        """
            Make a normal roll
        """
        parsed_commands = self.parse_text(text)
        if parsed_commands['weary']:
            skill_roll = self.get_weary_roll(parsed_commands['num_dice'])
        else:
            skill_roll = self.get_skill_roll(parsed_commands['num_dice'])
        feat_die = self.get_gm_feat_roll(parsed_commands['favored'])
        await ctx.send(embed=self.generate_gm_text_box(skill_roll, feat_die))

def setup(bot: commands.Bot):
    bot.add_cog(OneRingCommands(bot))