import discord

class MyUIClass(discord.ui.View):
  def __init__(self):
    super().__init__()

  @discord.ui.button(label="label", style=discord.ButtonStyle.success)
  async def my_interaction(self, button: discord.ui.Button, interaction: discord.Interaction):
    await interaction.response.send_message("complete")
    self.stop()