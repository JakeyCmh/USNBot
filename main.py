import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Constants for channel IDs
EVENT_LOG_CHANNEL_ID = 1207431833009258526
LOA_REQUEST_CHANNEL_ID = 1244764741419663501
QUOTA_WARNING_LOG_CHANNEL_ID = 1244431932377530388
ENSIGN_APPLICATION_CHANNEL_ID = 1203033921600888842
RESPONSE_CHANNEL_ID = 736871527470989366

# Ensign application button view
class EnsignButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.check_button = Button(label="Approve", style=discord.ButtonStyle.green, custom_id="approve")
        self.deny_button = Button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny")
        self.add_item(self.check_button)
        self.add_item(self.deny_button)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Application approved.", ephemeral=True)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Application denied.", ephemeral=True)

# Ping Command
@bot.tree.command(name="ping", description="funny admin aboose")
async def ping(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"{user.mention} :USNTrollage:", ephemeral=True)

# Event Log Command
@bot.tree.command(name="eventlog", description="Logging Events")
async def eventlog(interaction: discord.Interaction):
    # Create the modal for event log submission
    modal = Modal(title="Event Log Submission")
    modal.add_item(TextInput(label="Event Name", placeholder="ex. Patrol, Training, Etc."))
    modal.add_item(TextInput(label="Host", placeholder="Discord Username"))
    modal.add_item(TextInput(label="Date/Time? Include Timezone", placeholder="ex. 1/14/25 at 12:00 PM CST"))
    modal.add_item(TextInput(label="Attendees", placeholder="ex. Hilop33, Jakeycmh, etc."))
    modal.add_item(TextInput(label="Friendly & Enemy casualties", placeholder="ex. 1 friendly, 2 enemy"))
    await interaction.response.send_modal(modal)

    # Wait for modal submission (this is how we handle the modal results)
    def handle_submission(data):
        # Make sure to move the code that logs the event into an async function
        async def log_event():
            # Send the event log to the appropriate channel
            log_channel = bot.get_channel(EVENT_LOG_CHANNEL_ID)
            await log_channel.send(f"Event Log submitted by {interaction.user.mention}:\n"
                                   f"Event Name: {data['Event Name']}\n"
                                   f"Host: {data['Host']}\n"
                                   f"Date/Time: {data['Date/Time']}\n"
                                   f"Attendees: {data['Attendees']}\n"
                                   f"Friendly & Enemy casualties: {data['Friendly & Enemy casualties']}")
        # Call the async log_event function
        asyncio.create_task(log_event())

# LOA Request Command
@bot.tree.command(name="loarequest", description="Request a leave of absence")
async def loarequest(interaction: discord.Interaction):
    modal = Modal(title="LOA Request Form")
    modal.add_item(TextInput(label="Discord Username", placeholder="Discord Username here"))
    modal.add_item(TextInput(label="Reason for LOA Request", placeholder="ex. moving, vacation, etc."))
    modal.add_item(TextInput(label="Date & Time? INCLUDE TIMEZONE", placeholder="ex. 1/14/25 at 12:00 PM CST"))
    modal.add_item(TextInput(label="Length of LOA", placeholder="ex. 20 days, 30 days, etc."))
    modal.add_item(TextInput(label="Lower Quota Request", placeholder="If on LOA, specify quota"))
    await interaction.response.send_modal(modal)

    # Capture the submission of the modal and handle it properly
    def handle_submission(data):
        # Send the request into the LOA request channel
        async def submit_loa_request():
            loa_channel = bot.get_channel(LOA_REQUEST_CHANNEL_ID)
            await loa_channel.send(f"LOA Request from {interaction.user.mention}:\n"
                                   f"Username: {data['Discord Username']}\n"
                                   f"Reason: {data['Reason for LOA Request']}\n"
                                   f"Date & Time: {data['Date & Time']}\n"
                                   f"Length: {data['Length of LOA']}\n"
                                   f"Lower Quota Request: {data['Lower Quota Request']}")
        # Call the async submit_loa_request function
        asyncio.create_task(submit_loa_request())

# Quota Warning Command
@bot.tree.command(name="quotawarning", description="The command used by High Command to punish members for not reaching quota")
async def quotawarning(interaction: discord.Interaction, user: discord.User):
    # Send a DM to the user with the quota warning
    try:
        await user.send(f"{user.mention}, You have received a quota warning in the United States Navy | DSS Group due to failing to host the required amount of events.")
    except discord.Forbidden:
        # If the DM is disabled, send the message to the log channel
        log_channel = bot.get_channel(QUOTA_WARNING_LOG_CHANNEL_ID)
        embed = discord.Embed(title="Quota Warning", description=f"User ID: {user.id}\nUsername: {user.mention}\nDate: {discord.utils.utcnow()}")
        await log_channel.send(embed=embed)

# Ensign Application Embed Command
@bot.tree.command(name="ensignembed", description="Ensign Application Information")
async def ensignembed(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**Ensign Application Information**",
        description="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                    ":page_facing_up: ┃`About`\n"
                    "> Welcome to the United States Navy! In order to climb the ranks of our Navy, you must first pass a Basic Individual Readiness Battery assessment to ensure you are ready to perform as a sailor in the US Navy. **You can find all the information needed here.**\n"
                    "> We wish you the best of luck, and hope to see you around.\n\n"
                    ":busts_in_silhouette:┃`Chain Of Command`‎‎\n"
                    "> **Secretary of the Navy - Hilop33**\n"
                    "> **Undersecretary of the Navy - GamesWithJake1**\n"
                    "> **Assistant Secretary of the Navy - BigJack787**\n"
                    "> **Chief of Naval Personnel - Jakeycmh**\n"
                    "> **Chief of Naval Operations - BigJack787**\n\n"
                    ":link:┃`Important Links` ‎ ‎\n"
                    "> :floppy_disk: ┃**[USN Database](https://trello.com/b/iykqFez0/united-states-navy-database)**\n"
                    "> :anchor: ┃**[Fleet Database](https://trello.com/b/0qCF6E0I/united-states-navy-fleet-database)**\n"
                    "> :ship:┃**[Fleet Formations](https://docs.google.com/document/d/1vMVsWzYaKrf17RMbf87Jawo_dXNmRsTTyTqAXbi0RsA/edit?usp=sharing)**\n"
                    "> :crossed_swords:┃**[Rules Of Engagement](https://docs.google.com/document/d/1S4_wptsHZ1eGI7uMJrvz1trK9Va0yRRc42N1i8-yAHY/edit?usp=sharing)**\n"
                    "> :scales:┃**[Uniform Code Of Military Justice](https://docs.google.com/document/d/1-W6ow8lZ7UQN0eOXK_Edc7FWxSTT2WJMeD3HBmK3OhE/edit?usp=sharing)**\n"
                    "> :handshake:┃**[Allied Navies](https://discord.com/channels/736871527470989363/750521546258251876)**\n\n"
                    ":pencil:┃`Notes`\n"
                    "> **__Once you have familiarized yourself with these documents, take the test listed below.__**\n"
                    "> You must have at least an 80% score to pass.\n\n"
                    "> You may ping a Rear Admiral+ to grade your test if you get no response within 3 hours.\n"
                    "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
                    "> Once you fill in your answers press the \"Submit\" button.\n\n"
                    "> \"ROE\" in the application stands for Rules of Engagement. [**Document**](https://docs.google.com/document/d/1S4_wptsHZ1eGI7uMJrvz1trK9Va0yRRc42N1i8-yAHY/edit?usp=sharing) (Document linked above)"
    )
    embed.color = discord.Color(0x1E3A8A)

    # Post the embed to the ensign application channel
    channel = bot.get_channel(ENSIGN_APPLICATION_CHANNEL_ID)
    await channel.send(embed=embed, view=EnsignButtonView())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # Register slash commands here
    await bot.tree.sync()  # Synchronize the bot's commands with Discord
    print("Slash commands have been registered.")

# Run the bot with your token
bot.run("YOUR BOT ID")
