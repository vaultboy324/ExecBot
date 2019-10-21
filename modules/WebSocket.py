import websocket
import telebot
import json

from config import Config
from config import SocketActions

from entities.odata_requests import ODataRequests
from entities.user import User

from Constants import Constants

from keyboard.Keyboard import Keyboard

# from main import bot


class WebSocket:
    __ws = None
    __bot = None

    @staticmethod
    def get_json_from_pcp_message(message):
        start_json = message.find('{')
        end_json = len(message)

        result_string = message[start_json:end_json]

        parameters = json.loads(result_string)

        return parameters

    @staticmethod
    def on_message(ws, message: str):
        # bot.send_message()

        parameters = WebSocket.get_json_from_pcp_message(message)

        # telegram_id = parameters[Constants.telegram_id]

        if parameters[Constants.operation_type] == SocketActions.S_SEND_NOTIFY:
            keyboard = Keyboard.get_main_keyboard()

            telegram_id = parameters[Constants.telegram_id]
            WebSocket.__bot.send_message(telegram_id, "Регистрация завершена! Приятного использования", reply_markup=keyboard)

        elif parameters[Constants.operation_type] == SocketActions.S_SEND_STICKER:
            user_table = parameters[Constants.user_table]
            for user in user_table:
                telegram_id = user[Constants.telegram_id]
                WebSocket.get_bot().send_sticker(telegram_id, Config.STICKER_CODE)

        elif parameters[Constants.operation_type] == SocketActions.S_SEND_RESET_REQUEST:
            telegram_id = parameters[Constants.telegram_id]
            session_guid = parameters[Constants.session_guid]

            user = User(telegram_id)
            user.set_session(session_guid)

            keyboard = Keyboard.get_reset_keyboard(user)
            WebSocket.__bot.send_message(telegram_id, "Выберите действие", reply_markup=keyboard)

    @staticmethod
    def create_connection():
        session = ODataRequests.create_user_session()

        WebSocket.__ws = websocket.WebSocketApp(Config.SOCKET_LINK, header=session.headers, subprotocols=Config.SUBPROTOCOLS,
                                    on_message=WebSocket.on_message)

    @staticmethod
    def set_bot(bot: telebot.TeleBot):
        WebSocket.__bot = bot

    @staticmethod
    def get_bot():
        return WebSocket.__bot

    @staticmethod
    def listen():
        WebSocket.__ws.run_forever()