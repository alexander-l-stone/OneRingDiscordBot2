from discord.ext import commands
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
                d6 = 0
            die_array.append(d6)
        return die_array
    
    def get_player_feat_roll(self, favored: int):
        """
            Rolls a feat die. If favored is < 1, this roll is unfavored.
            If favored is > 1, roll is favored.
        """
        original_roll = randint(1, 12)
        if original_roll == 11:
            original_roll = 0
        if favored != 0:
            second_roll = randint(1, 12)
            if second_roll == 11:
                second_roll = 0
        if favored > 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return max(original_roll, second_roll)
        if favored < 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return min(original_roll, second_roll)
        return original_roll
    
    def get_gm_feat_roll(self, favored: int):
        """
            Rolls a feat die. If favored is < 1, this roll is unfavored.
            If favored is > 1, roll is favored.
        """
        original_roll = randint(1, 12)
        if original_roll == 12:
            original_roll = 0
        if favored != 0:
            second_roll = randint(1, 12)
            if second_roll == 12:
                second_roll = 0
        if favored > 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return max(original_roll, second_roll)
        if favored < 0:
            print(f"Original Roll: {original_roll}, Second Roll: {second_roll}")
            return min(original_roll, second_roll)
        return original_roll

    def generate_player_text_box(self, skill_roll, feat_die):
        print_string = 'Skill Dice: '
        total = 0
        num_sixes = 0
        for num in skill_roll:
            total += num
            print_string = f"{print_string}{num} "
            if num == 6:
                num_sixes += 1
        total += feat_die
        print_string = f"{print_string}| Feat Die: {feat_die} |"
        if feat_die == 12:
            print_string = f"{print_string} Automatic Success |"
        print_string = f"{print_string} Total: {total} | You rolled {num_sixes} 6's"
        return print_string
    
    def generate_gm_text_box(self, skill_roll, feat_die):
        print_string = 'Skill Dice: '
        total = 0
        num_sixes = 0
        for num in skill_roll:
            total += num
            print_string = f"{print_string}{num} "
            if num == 6:
                num_sixes += 1
        total += feat_die
        print_string = f"{print_string}| Feat Die: {feat_die} |"
        if feat_die == 11:
            print_string = f"{print_string} Automatic Success |"
        print_string = f"{print_string} Total: {total} | You rolled {num_sixes} 6's"
        return print_string

    def parse_text(self, text: str):
        text_array = text.split(' ')
        commands = {'favored': 0, 'weary': False, 'num_dice': 0}
        for text in text_array:
            if text == 'favored':
                commands['favored'] += 1
            elif text == 'unfavored':
                commands['favored'] -= 1
            elif text == 'weary':
                commands['weary'] = True
            elif text.isnumeric():
                commands['num_dice'] += int(text)
        return commands

    @commands.command(name="roll")
    async def roll(self, ctx: commands.Context, *, text: str):
        """
            Make a normal roll
        """
        parsed_commands = self.parse_text(text)
        print(parsed_commands)
        if parsed_commands['weary']:
            skill_roll = self.get_weary_roll(parsed_commands['num_dice'])
        else:
            skill_roll = self.get_skill_roll(parsed_commands['num_dice'])
        feat_die = self.get_player_feat_roll(parsed_commands['favored'])
        await ctx.send(self.generate_player_text_box(skill_roll, feat_die))
    
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
        await ctx.send(self.generate_gm_text_box(skill_roll, feat_die))

def setup(bot: commands.Bot):
    bot.add_cog(OneRingCommands(bot))