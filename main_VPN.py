import logging
import csv
import outlook

mail = outlook.Outlook()
mail.login('sysmantc5@outlook.com','pass')
lista=None
with open("pines.csv", 'r') as data:
  
    lista=list(csv.DictReader(data))
        
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import base64
from email.mime.text import MIMEText
from requests import HTTPError

#SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
#flow = InstalledAppFlow.from_client_secrets_file('client_secret_483423179538-bemkc5degba02oj0smmqe32ka55fkdrq.apps.googleusercontent.com.json', SCOPES)
#creds = flow.run_local_server(port=0)

#service = build('gmail', 'v1', credentials=creds)



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, sendMailTo, = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

keyboard_provider = [
        [InlineKeyboardButton("CAD", callback_data="CAD"),],
        [InlineKeyboardButton("C5", callback_data="C5"),],
        [InlineKeyboardButton("revisar bandeja", callback_data=str(TWO)),]
    ]
reply_markup_provider = InlineKeyboardMarkup(keyboard_provider)

keyboard_CAD = [
    [InlineKeyboardButton("Sergio Fernandez", callback_data="User: sfernandez \n Email: sfernandez@totalplay.com.mx")],
    [InlineKeyboardButton("Marco Yañez", callback_data="User: myanez \n Email: myanez@promad.com.mx")],
    [InlineKeyboardButton("Daniel Espinoza", callback_data="User: iespinosa \nEmail: iespinosa@promad.com.mx")],
    [InlineKeyboardButton("Narciso Cantero", callback_data="User: ncanterom \nEmail: ncantero@promad.com.mx")],
    [InlineKeyboardButton("Miguel de la Rosa", callback_data="User: mrosa \nEmail: mrosa@promad.com.mx")],
    [InlineKeyboardButton("Sergio Neri", callback_data="User: sneri \nEmail: sneri@promad.com.mx")],
    [InlineKeyboardButton("Gibran Cruz", callback_data="User: gcruz \nEmail: gcruz@totalplay.com.mx")],
    [InlineKeyboardButton("Luis Aguilar", callback_data="User: laguilar \nEmail: laguilar@promad.com.mx")],
]
reply_markup_CAD = InlineKeyboardMarkup(keyboard_CAD)

keyboard_C5 = [
    [InlineKeyboardButton("Daniel Rivero", callback_data="User: driveroe \n Email: driveroe@c5.cdmx.gob.mx")],
    [InlineKeyboardButton("Adrian Gamero", callback_data="User: myanez \n Email: myanez@promad.com.mx")],
    [InlineKeyboardButton("Marcos Espinoza", callback_data="User: iespinosa \nEmail: iespinosa@promad.com.mx")],
    [InlineKeyboardButton("Daniel Carrasco", callback_data="User: ncanterom \nEmail: ncantero@promad.com.mx")],
    [InlineKeyboardButton("Diana Hilario", callback_data="User: mrosa \nEmail: mrosa@promad.com.mx")],
    [InlineKeyboardButton("Osvaldo Hernandez", callback_data="User: sneri \nEmail: sneri@promad.com.mx")],
    #[InlineKeyboardButton("Gibran Cruz", callback_data="User: gcruz \nEmail: gcruz@totalplay.com.mx")],
    #[InlineKeyboardButton("Luis Aguilar", callback_data="User: laguilar \nEmail: laguilar@promad.com.mx")],
]
reply_markup_C5 = InlineKeyboardMarkup(keyboard_C5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
 
    await update.message.reply_text("a que area le generamos la VPN?", reply_markup=reply_markup_provider )
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES




async def cad_prov(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()


    await query.edit_message_text(
        text="quien requiere la vpn?", reply_markup=reply_markup_CAD
    )
    return sendMailTo
async def vpnC5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="quien requiere la vpn?", reply_markup=reply_markup_C5
    )
    return sendMailTo
async def revisarMail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    #mail.login('sysmantc5@outlook.com','system2137c5@')
    mail.inbox()
    texto=mail.unread()
    replyText="no se encontro un nuevo mail"
    if(texto==None):
        replyText="no se encontro un nuevo mail"
    else:
        if("Ejemplo de autenticación" in texto):
            aux= str(texto).split("Ejemplo de autenticación")
            aux=aux[0].replace("▉","")
            aux=aux.splitlines();
            replyText=""
            username=None
            for line in aux:
                if("Username"  in line):
                    username=line.split("Username: ")
                    username=username[1]
                    print(username)

                    replyText=replyText+line+"\n"
                if("Password"  in line):
                    for dict in lista:
                        if(dict["user"]==username):
                            pin=dict["pin"]
                            replyText=replyText+line+pin
    await query.edit_message_text(
        text=replyText, reply_markup=None
    )
    return ConversationHandler.END





async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    data1 =query.data
    #mail.sendEmail( "daniel.rivero132@gmail.com", "VPN", data1)
    await query.edit_message_text(text=f"Se ha enviado el mail con \n{data1}")

    #mail.sendEmailMIME( "daniel.rivero132@gmail.com", "VPN", data1)
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6289693606:AAGzO-TnTtoGIKLoAlhMpcleEqALKoxmxRM").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(cad_prov, pattern="^CAD$"),
                CallbackQueryHandler(vpnC5, pattern="^C5$"),
                CallbackQueryHandler(revisarMail, pattern="^"+str(TWO)+"$"),
            ],
            sendMailTo: [
                CallbackQueryHandler(end),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()