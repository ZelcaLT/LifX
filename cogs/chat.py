import nextcord
import nltk
nltk.download('omw-1.4')
from nextcord.ext import commands
from neuralintents import GenericAssistant

class ChatBot(commands.Cog, name="🤖Chatbot"):
    def __init__(self, bot): 
        self.bot = bot 
        self.bot.chatbot = GenericAssistant("intents.json")
        self.bot.chatbot.train_model()
        self.bot.chatbot.save_model()
        
    @commands.Cog.listener()
    async def on_message(self, message): 
        if message.author == self.bot.user:
            return
        
        if message.content.startswith("ai "):
            response = self.bot.chatbot.request(message.content[4:])
            await message.channel.send(response)
            
def setup(bot):
    bot.add_cog(ChatBot(bot))