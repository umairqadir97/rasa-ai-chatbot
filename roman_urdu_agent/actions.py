from __future__ import absolute_import, division, unicode_literals
import re
import csv
from rasa_sdk import Action
from sample_data import *
from rasa_sdk.forms import FormAction
from rasa.core.policies.policy import confidence_scores_for
from rasa_sdk.events import SlotSet, ConversationPaused, ReminderScheduled, ConversationResumed
import random
from datetime import datetime, timedelta, date
from default_configurations import *


##########################
# GENERAL
###########################

# Intent: greetings.hello
class HelloAndGreetings(Action):
    def name(self):
        return 'action_hello_user'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            authenticated_user_response_templates = ["Hi {user_name}, telenor customer care me khushamdeed!",
                                                     "Hey {user_name}, me ap ki kesy madad kr skta hu?"]
            user_name = ""
            if mobile_number in user_data.keys():
                user_name = single_user_object['name']
            response = random.choice(authenticated_user_response_templates)
            dispatcher.utter_message(response.format(user_name=user_name))
            # image_url = "http://crm2.univ-lorraine.fr/pages_perso/Aubert/FTenglish/conv2d/hello.jpg"
            # image_url = "./assets/telenor_pakistan.png"
            # image_url = "https://i.ibb.co/qMFfqnF/telenor-pakistan.png"
            # message = {"image_url": image_url}
            # dispatcher.utter_custom_json(message)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with HelloAndGreetings: {}".format(e))
        return None


class ActionIntermediateFallback(Action):
    def name(self):
        return "action_default_ask_affirmation"

    def __init__(self):
        self.intent_mappings = {}
        # read the mapping and store it in a dictionary
        with open("intent_csv_mapping.txt", "r") as file:
            lines = file.read().split("\n")
            for line in lines:
                splits = line.split(":")
                if len(splits) > 1:
                    self.intent_mappings[splits[0]] = splits[0]

    def run(self, dispatcher, tracker, domain):
        last_intent = tracker.latest_message['intent']['name']
        last_intent_confidence = tracker.events[-1]['parse_data']['intent']['confidence']
        if last_intent_confidence < 0.3 or last_intent in [None, 'out_of_scope']:
            response = "Please apna swal dobara likhain!"
            dispatcher.utter_message(response)
            # todo: status of consecuive_fallback slot?
        else:
            # sorted(tracker.latest_message['intent_ranking'], key=lambda x: x['confidence'], reverse=True)[0]
            message = "Kia apka swla ye ha '{}'?".format(last_intent)
            buttons = [{'title': 'Yes',
                        'payload': '/{}'.format(last_intent)},
                       {'title': 'No',
                        'payload': '/out_of_scope'}]
            dispatcher.utter_button_message(message, buttons=buttons)
        # dispatcher.utter_message(message)
        return []


# Intent: CustomFallBackAction
def get_action_names():
    with open("domain.yml", "r") as file:
        text = file.read()
    return [action.replace("- ", "") for action in text.split("actions:")[1].split(":")[0].split("\n")[:-1] if action]


class CustomFallback(Action):
    def name(self):
        return 'action_custom_fallback'

    def run(self, dispatcher, tracker, domain):
        try:
            consecutive_fallback = tracker.get_slot("number_of_fallbacks")
            consecutive_fallback += 1.0
            previous_actions = [event['name'] for event in tracker.events if 'name' in event and
                                event['name'] in get_action_names()]
            response = default_fallback_response
            if previous_actions[-1] == "action_custom_fallback":
                if consecutive_fallback >= 2.0:
                    # todo: this below mentioned response is being used in "api.get_server_response" & in LiveZilla UI
                    print("Consecutive Fallbacks: ", consecutive_fallback)
                    response = "Sorry, mje apka swal samj ni aa rha. Thora intezar krain, apki drkhwast mutalqa expert to transfer ki ja rhi ha..."
                    consecutive_fallback = 0.0
                    dispatcher.utter_message(response)
                    return [SlotSet("number_of_fallbacks", consecutive_fallback)]
            else:
                # not consecutive fallback
                consecutive_fallback = 0.0
            dispatcher.utter_message(response)
            return [SlotSet("number_of_fallbacks", consecutive_fallback)]
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with CustomFallback: {}".format(e))
        return None


# Intent: offers.info
class OffersInformation(Action):
    def name(self):
        return 'action_offers_info'

    def run(self, dispatcher, tracker, domain):
        try:
            response = "here are available offers:"
            dispatcher.utter_message(response)
            offer_image_url = "https://i.ibb.co/BLYpFSB/whatsapp-offer-256x256.png"
            offer_details_url = "https://i.ibb.co/dm74DPP/whatsapp-offer-details-256x256.png"
            dispatcher.utter_custom_json({"image_url": offer_image_url})
            dispatcher.utter_custom_json({"image_url": offer_details_url})
            dispatcher.utter_message("Ye offer hadil krny k lye 'YES' likhain.")
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with OffersInformation: {}".format(e))
        return None


# Intent: offers.info -- subscribe
class OfferSubscribe(Action):
    def name(self):
        return 'action_offers_subscribe'

    def run(self, dispatcher, tracker, domain):
        try:
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                response = "You have successfully availed this offer."
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with OfferSubscribe: {}".format(e))
        return None

##########################
# USER VERIFICATION
###########################
# Intent: authenticate user !
class ActionVerificationForm(FormAction):
    def name(self):
        return "action_verification_required"

    @staticmethod
    def required_slots(tracker):
        return ["mobile_number", "pin"]

    def slot_mappings(self):
        return {
            "mobile_number": self.from_text(intent=None),
            "pin": self.from_text(intent=None)
        }

    def submit(self, dispatcher, tracker, domain):
        # get first match from input text
        mobile_number = re.search(r'(((034)|(9234))[0-9][-_. ]*[0-9]*)', tracker.get_slot("mobile_number"))
        pin = re.search(r'[0-9]*', tracker.get_slot("pin"))

        if mobile_number and pin:
            pin = pin.group(0)
            mobile_number = re.sub(r'[-_.+]', '', mobile_number.group(0))
            # mobile_number = re.sub(r'^034', '9234', mobile_number)   # standardize ot 9234x.......
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')

            if mobile_number in user_data.keys() and len(pin) == 4:
                dispatcher.utter_message("\nHi {}, ap is mobile_number:{} k lye verify ho gye hain!".format(
                    user_data[mobile_number]['name'], mobile_number))
                return [SlotSet('verification', "yes"), SlotSet('mobile_number', mobile_number), SlotSet('pin', pin)]
            elif mobile_number not in user_data.keys():
                dispatcher.utter_message("Sorry, is mobile number ka koi record ni ha.")
            elif len(pin) != 4:
                dispatcher.utter_message("Invalid PIN")
        # todo: this response is being used in 'chat_endpoint.get_response_from_chatbot', be cautious!
        dispatcher.utter_message("Authentication fail ho gye ha. apni request dobara enter krain")
        return [SlotSet('verification', "no")]


##########################
# BALANCE
###########################
# Intent: balance_info.info
class BalanceInformation(Action):
    def name(self):
        return 'action_balance_info'
    # [event['parse_data']['entities'] for event in tracker.events if 'parse_data' in event.keys()]

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                balance = tracker.get_slot("current_balance_value")
                balance_validity = tracker.get_slot("current_balance_validity")
                response = "Ap ka maujoda balance: Rs. {balance}, validity: {balance_validity}".format(
                    balance=balance, balance_validity=balance_validity)
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with BalanceInformation: {}".format(e))
        return None


# Intent: balance_info.info
class BalanceExpiry(Action):
    def name(self):
        return 'action_balance_expiry'

    def run(self, dispatcher, tracker, domain):
        try:
            # check if balance slot is filled:
            # e.g. "expiry", "balance expiry", "akhri tareekh" ??
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                balance_validity = tracker.get_slot("current_balance_validity")
                response = "Ap ka balance khatam hony ki akhri tareekh: {balance_validity}".format(
                    balance_validity=balance_validity)
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with BalanceExpiry: {}".format(e))
        return None


# Intent: balance.balance_usage
class BalanceUsage(Action):
    def name(self):
        return 'action_balance_usage_report'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                balance_usage = tracker.get_slot("current_balance_usage")
                response = "Ap ab tak Rs.{balance_usage} ka balance use chuky hain.".format(balance_usage=balance_usage)
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with BalanceExpiry: {}".format(e))
        return None


##########################
# LAST RECHARGE
###########################
# Intent: last_recharge.info
class LastRechargeInfo(Action):
    def name(self):
        return 'action_last_recharge_info'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                balance = tracker.get_slot("current_balance_value")
                balance_validity = tracker.get_slot("current_balance_validity")
                response = """Pichli bar ap ny {last_recharge} ka recharge karwaya tha.
                AP ka maujoda balance Rs. {balance} ha, validity {balance_validity}""".format(
                    last_recharge=single_user_object['last_recharge'],
                    balance=balance,
                    balance_validity=balance_validity
                )
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with LastRechargeInfo: {}".format(e))
        return None


# Intent: last_recharge.date
class LastRechargeDate(Action):
    def name(self):
        return 'action_last_recharge_date'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                response = "Pichli bar ap ny {last_recharge} ka recharge karwaya tha.".format(
                    last_recharge=single_user_object['last_recharge'])
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with LastRechargeDate: {}".format(e))
        return None


###########################
# EMERGENCY LOAN
###########################
# Intent: emergency_loan.subscribe
class EmergencyLoanCurrentStatus(Action):
    def name(self):
        return 'action_emergency_loan_current_status'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                loan_service_status = tracker.get_slot("loan_service_status")
                response = """Sorry, ap ne Rs.20 ka pichla emergency loan wapis nhi kia abi.
                Ap agly recharge tak mazeed loan nhi le sakty."""
                if loan_service_status == "unsubscribed":
                    response = "Ap ne emergency loan subscribe nhi kia. Abi Rs.20 ka Loan leny k lye 'YES' likhy."
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with EmergencyLoanCurrentStatus: {}".format(e))
        return None


# Intent: emergency_loan.subscribe
class EmergencyLoanSubscribe(Action):
    def name(self):
        return 'action_emergency_loan_subscribe'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                loan_service_status = tracker.get_slot("loan_service_status")
                loan_last_availed = tracker.get_slot("loan_last_availed")
                current_balance = tracker.get_slot("current_balance_value")
                # balance_usage = tracker.get_slot("current_balance_usage")
                balance_validity = tracker.get_slot("current_balance_validity")
                response = "Sorry, ap ne pichla emergency loan wapis nhi kia abi. Ap mazeed loan nhi hasil kr sakty!"

                if loan_service_status == "unsubscribed":
                    loan_service_status = "subscribed"
                    loan_last_availed = str(date.today())
                    response = "Ap ne kamyabi sy Rs.20. ka emergency loan hasil kr lia ha."
                    current_balance += 20.0
                    balance_validity = "15-01-2020 "
                dispatcher.utter_message(response)
                return [SlotSet("loan_service_status", loan_service_status),
                        SlotSet("loan_last_availed", loan_last_availed),
                        SlotSet("current_balance_value", current_balance),
                        SlotSet("current_balance_validity", balance_validity)]
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with EmergencyLoanSubscribe: {}".format(e))
        return None


# Intent: emergency_loan.subscribe
class EmergencyLoanLastAvailed(Action):
    def name(self):
        return 'action_emergency_loan_last_availed'

    def run(self, dispatcher, tracker, domain):
        try:
            mobile_number = tracker.get_slot("mobile_number")
            if mobile_number and mobile_number.startswith('034'):
                mobile_number = mobile_number.replace('034', '9234')
            verification_status = tracker.get_slot("verification")
            if verification_status == "yes":
                loan_last_availed = tracker.get_slot("loan_last_availed")
                response = "Ap ny {} ko Rs.20 emergency loan lia tha.".format(loan_last_availed)
                dispatcher.utter_message(response)
        except Exception as e:
            dispatcher.utter_message("Sorry, Something went wrong. Apna swal dobara enter krain")
            print("\nERROR: Something went wrong with EmergencyLoanLastAvailed: {}".format(e))
        return None
