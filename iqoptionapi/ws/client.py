"""Module for IQ option websocket."""

import json
import logging
import websocket
import iqoptionapi.constants as OP_code
import iqoptionapi.global_value as global_value



class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)
    def dict_queue_add(self,dict,maxdict,key1,key2,key3,value):
        if key3 in dict[key1][key2]:
                    dict[key1][key2][key3]=value
        else:
            while True:
                try:
                    dic_size=len(dict[key1][key2])
                except (KeyError, TypeError) as e:
                    logger = logging.getLogger(__name__)
                    logger.debug(f"Dictionary structure not as expected: {e}")
                    dic_size=0
                if dic_size<maxdict:
                    dict[key1][key2][key3]=value
                    break
                else:
                    #del mini key
                    del dict[key1][key2][sorted(dict[key1][key2].keys(), reverse=False)[0]]

    def on_message(self, ws, message):
        """Method to process websocket messages."""
        global_value.ssl_Mutual_exclusion = True
        logger = logging.getLogger(__name__)

        try:
            # Check if message is a WebSocketApp object (which happens sometimes)
            if isinstance(message, websocket.WebSocketApp):
                logger.error("Received WebSocketApp object as message")
                logger.debug(f"Raw message: {message}")
                global_value.ssl_Mutual_exclusion = False
                return

            # Handle binary messages
            if isinstance(message, bytes):
                try:
                    message = message.decode('utf-8')
                except UnicodeDecodeError as e:
                    logger.error(f"Failed to decode binary message: {e}")
                    logger.debug(f"Raw binary message: {message}")
                    global_value.ssl_Mutual_exclusion = False
                    return

            # Log raw message for debugging
            logger.debug(f"Raw message received: {message}")

            # Check if message is empty or whitespace
            if not message or (isinstance(message, str) and message.isspace()):
                logger.error("Received empty message from websocket")
                global_value.ssl_Mutual_exclusion = False
                return

            # Handle string messages that might be already JSON
            if isinstance(message, str):
                try:
                    if message.startswith('{') or message.startswith('['):
                        parsed_message = json.loads(message)
                    else:
                        logger.error(f"Invalid JSON format: {message[:100]}...")
                        global_value.ssl_Mutual_exclusion = False
                        return
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    logger.debug(f"Failed message: {message[:100]}...")
                    global_value.ssl_Mutual_exclusion = False
                    return
            else:
                logger.error(f"Unexpected message type: {type(message)}")
                global_value.ssl_Mutual_exclusion = False
                return

            # Validate message structure
            if not isinstance(parsed_message, dict) or "name" not in parsed_message:
                logger.error("Message missing required 'name' field")
                logger.debug(f"Invalid message structure: {parsed_message}")
                global_value.ssl_Mutual_exclusion = False
                return

            # Process the parsed message
            message = parsed_message  # Replace the raw message with parsed version

            if message["name"] == "timeSync":
                self.api.timesync.server_timestamp = message["msg"]
            elif message["name"] == "profile":
                self.api.profile.msg = message["msg"]
                # Set balance_id if not already set
                try:
                    if global_value.balance_id is None:
                        for balance in message["msg"]["balances"]:
                            if balance["type"] == 4:  # Practice account
                                global_value.balance_id = balance["id"]
                                break
                        if global_value.balance_id is None and len(message["msg"]["balances"]) > 0:
                            # If no practice account found, use the first balance
                            global_value.balance_id = message["msg"]["balances"][0]["id"]

                    # Also set the balance_id in the profile object
                    self.api.profile.balance_id = message["msg"]["balance_id"]
                except Exception as e:
                    logger = logging.getLogger(__name__)
                    logger.debug(f"Error setting profile balance_id: {e}")
            elif message["name"] == "candles":
                self.api.candles.candles_data = message["msg"]["data"]
            elif message["name"] == "balance":
                balance = message["msg"]
                if isinstance(balance, dict):
                    self.api.profile.balance = balance
            elif message["name"] == "balances":
                self.api.balances_raw = message
            elif message["name"] == "instruments":
                self.api.instruments = message
            elif message["name"] == "financial-information":
                self.api.financial_information = message
            elif message["name"] == "position-changed":
                self.api.position_changed = message
            elif message["name"] == "option":
                self.api.order_data = message
            elif message["name"] == "positions":
                self.api.positions = message
            elif message["name"] == "position":
                self.api.position = message
            elif message["name"] == "deferred-orders":
                self.api.deferred_orders = message
            elif message["name"] == "position-history":
                self.api.position_history = message
            elif message["name"] == "history-positions":
                self.api.position_history_v2 = message
            elif message["name"] == "available-leverages":
                self.api.available_leverages = message
            elif message["name"] == "order-canceled":
                self.api.order_canceled = message
            elif message["name"] == "position-closed":
                self.api.close_position_data = message
            elif message["name"] == "overnight-fee":
                self.api.overnight_fee = message
            elif message["name"] == "api_option_init_all_result":
                self.api.api_option_init_all_result = message
            elif message["name"] == "initialization-data":
                self.api.api_option_init_all_result_v2 = message
            elif message["name"] == "underlying-list":
                self.api.underlying_list_data = message
            elif message["name"] == "strike-list":
                self.api.strike_list = message
            elif message["name"] == "api_game_getoptions_result":
                self.api.api_game_getoptions_result = message
            elif message["name"] == "sold-options":
                self.api.sold_options_respond = message
            elif message["name"] == "tpsl-changed":
                self.api.tpsl_changed_respond = message
            elif message["name"] == "auto-margin-call-changed":
                self.api.auto_margin_call_changed_respond = message
            elif message["name"] == "digital-option-placed":
                self.api.digital_option_placed_id = message["msg"]["id"]
            elif message["name"] == "result":
                self.api.result = message
            elif message["name"] == "instrument-quotes-generated":
                try:
                    active_id = message["msg"]["active"]
                    active = list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(active_id)]
                    size = message["msg"]["size"]
                    self.api.instrument_quites_generated_timestamp[active][size] = message["msg"]["timestamp"]
                    self.api.instrument_quites_generated_data[active][size] = message["msg"]["quotes"]
                    self.api.instrument_quotes_generated_raw_data[active][size] = message
                except:
                    pass
            elif message["name"] == "training-balance-reset":
                self.api.training_balance_reset_request = message["msg"]["isSuccessful"]
            elif message["name"] == "leaderboard-deals-client":
                self.api.leaderboard_deals_client = message["msg"]
            elif message["name"] == "commission-changed":
                try:
                    instrument_type = message["msg"]["instrument_type"]
                    active_id = message["msg"]["active_id"]
                    active = list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(active_id)]
                    self.api.subscribe_commission_changed_data[instrument_type][active] = message["msg"]["commission"]["value"]
                except:
                    pass
            elif message["name"] == "user-profile-client":
                self.api.user_profile_client = message["msg"]
            elif message["name"] == "leaderboard-userinfo-deals-client":
                self.api.leaderboard_userinfo_deals_client = message["msg"]
            elif message["name"] == "users-availability":
                self.api.users_availability = message["msg"]

        except Exception as e:
            logger.error(f"Unexpected error in on_message: {e}")
            logger.debug(f"Message that caused error: {message}")
            global_value.ssl_Mutual_exclusion = False
            return
        finally:
            global_value.ssl_Mutual_exclusion = False


    @staticmethod
    def on_error(ws, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)

        # Check if the error is related to receiving HTML instead of websocket handshake
        error_str = str(error)
        if "Handshake status" in error_str and "<!doctype html>" in error_str:
            logger.error("Received HTML page instead of websocket handshake. The websocket endpoint might be incorrect.")
            global_value.websocket_error_reason = "Received HTML page instead of websocket handshake. The websocket endpoint might be incorrect."
        else:
            global_value.websocket_error_reason = error_str

        global_value.check_websocket_if_error = True
    @staticmethod
    def on_open(ws): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect=1
    @staticmethod
    def on_close(ws, close_status_code, close_msg): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect=0
