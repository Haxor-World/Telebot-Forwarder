import telebot
import configparser
import os
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

config = configparser.ConfigParser()
config['CONFIGURATION'] = {
    'TOKEN': 'TELEGRAM_BOT_TOKEN',
    'ALLOWED_USER': "USER_ID1,USER_ID2,USER_ID3",
    'CHANNEL': 'CHANNEL_NAME'
}
config.read("config.ini")

console = Console()
channel = config["CONFIGURATION"]["CHANNEL"]
allowed_user = config["CONFIGURATION"]["ALLOWED_USER"]
bot = telebot.TeleBot(config["CONFIGURATION"]["TOKEN"])
member = allowed_user.split(",")

print(Panel.fit(
    """
[bold blue]Coded By[/bold blue] [bold red]@Real_Zeru_nishimura[/bold red]
[bold cyan]Token :[/bold cyan] [bold green]{0}[/bold green]
[bold cyan]Channel :[/bold cyan] [bold green]{1}[/bold green]
""".format(config["CONFIGURATION"]["TOKEN"], channel), title="Telegram Bot"))

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Allowed User", style="dim")
for x in member:
    table.add_row(x)
console.print(table)


def check_credentials(user):
    global member
    if user in member:
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
/ft - Forward Text
/fp - Forward Photo
/fv - Forward Video
/fd - Forward Document
""")

# Forwarding messages to the channel


@bot.message_handler(commands=['ft'])
def forward(message):
    check = check_credentials(message.from_user.username)
    if check == True:
        msg = "{0} \n\n Posted By @{1}".format(
            message.reply_to_message.text, message.from_user.username)
        if message.reply_to_message is not None:
            bot.send_message(channel, msg)
            bot.reply_to(message, "Message Forwarded")
        else:
            bot.reply_to(message, "Reply to a message to forward it")
    else:
        bot.reply_to(message, "You are not allowed to use this bot , Ur Username {0}".format(
            message.from_user.username))


@bot.message_handler(commands=['fp'])
def forward(message):
    check = check_credentials(message.from_user.username)
    if check == True:
        if message.reply_to_message is not None:
            if message.reply_to_message.content_type == "photo":
                bot.send_photo(chat_id=channel, photo=message.reply_to_message.photo[0].file_id, caption="{0} \n\n Posted By @{1}".format(
                    message.reply_to_message.caption if message.reply_to_message.caption is not None else "", message.from_user.username))
                bot.reply_to(message, "Message Forwarded")
            else:
                bot.reply_to(message, "Unknown Content Type")
        else:
            bot.reply_to(message, "Reply to a message to forward it")
    else:
        bot.reply_to(message, "You are not allowed to use this bot , Ur Username {0}".format(
            message.from_user.username))


@bot.message_handler(commands=['fv'])
def forward(message):
    check = check_credentials(message.from_user.username)
    if check == True:
        if message.reply_to_message is not None:
            if message.reply_to_message.content_type == "video":
                bot.send_video(chat_id=channel, video=message.reply_to_message.video.file_id, caption="{0} \n\n Posted By @{1}".format(
                    message.reply_to_message.caption if message.reply_to_message.caption is not None else "", message.from_user.username))
                bot.reply_to(message, "Message Forwarded")
            else:
                bot.reply_to(message, "Unknown Content Type")
        else:
            bot.reply_to(message, "Reply to a message to forward it")
    else:
        bot.reply_to(message, "You are not allowed to use this bot , Ur Username {0}".format(
            message.from_user.username))


@bot.message_handler(commands=['fd'])
def forward(message):
    check = check_credentials(message.from_user.username)
    if check == True:
        if message.reply_to_message is not None:
            if message.reply_to_message.content_type == "document":
                bot.send_document(chat_id=channel, document=message.reply_to_message.document.file_id, caption="{0} \n\n Posted By @{1}".format(
                    message.reply_to_message.caption if message.reply_to_message.caption is not None else "", message.from_user.username))
                bot.reply_to(message, "Message Forwarded")
            else:
                bot.reply_to(message, "Unknown Content Type")
        else:
            bot.reply_to(message, "Reply to a message to forward it")
    else:
        bot.reply_to(message, "You are not allowed to use this bot , Ur Username {0}".format(
            message.from_user.username))


if __name__ == '__main__':
    if os.path.isfile("config.ini"):
        console.print("[bold green]Config File Found[/bold green]")
        print("[bold green]Bot Started[/bold green]")
    else:
        with open("config.ini", "w") as configfile:
            config.write(configfile)
            console.print("[bold red]Config File Created[/bold red]")
    bot.infinity_polling()
