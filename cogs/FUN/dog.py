import nextcord, requests
from nextcord.ext import commands

class Dog(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @nextcord.slash_command(description="Will send a dog pic for you!")
  async def dog(self, interaction: nextcord.Interaction):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    image_link = response.json()["message"]
    await interaction.response.send_message(image_link)

def setup(client):
  client.add_cog(Dog(client))