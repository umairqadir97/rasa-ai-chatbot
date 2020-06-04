combo_packages = {
    "Freedom600": {
        "onnet": "2,000",
        "offnet": "300 Mins",
        "sms": "2,000",
        "data": "6,000 MBs",
        "price": "Rs. 750 Incl. Tax",
        "validity_in_days": "30"
    },
    "Freedom1000": {
        "onnet": "unlimited",
        "offnet": "500 Mins",
        "sms": "8000",
        "data": "12000 MBs",
        "price": "Rs. 1250 Incl. Tax",
        "validity_in_days": "30"
    },
    "Freedom1500": {
        "onnet": "unlimited",
        "offnet": "800 Mins",
        "sms": "15,000",
        "data": "32000 MBs",
        "price": "Rs. 1850 Incl. Tax",
        "validity_in_days": "30"
    }
}

add_on_sms_packages = {
    "Smart1000": {
        "sms_allowed": 8000,
        "price": 200,
        "validity_in_days": 30
    },
    "Smart1500": {
        "sms_allowed": 10000,
        "price": 300,
        "validity_in_days": 30
    },
    "Smart3000": {
        "sms_allowed": "unlimited",
        "price": 500,
        "validity_in_days": 30
    }
}

# add-on offers responses
roaming_offers_available = """Ap k account k lye International Roaming Service me ye offers available hain:
Global-Bundle(price: Rs. 2000, internet: 1000 MBs, Voice(Incoming/Outgoing): 20 Min, SMS: 20, Validity: 7 days).\n
Global-UK-US-Mega-Bundle(price: Rs. 999, internet: 1000 MBs, Validity: 30 days).\n
Mini-Bundle-Turkey(price: Rs. 200, internet: 100 MBs, Validity: 30 days)."""

active_roaming_response = """Ap ki international roaming service is waqt ON ha. 
Ap k pas International Roaming me 10 minutes, 15 SMS & 500 MBs hain, validity 15-12-2019."""

non_active_roaming_response = """Ap ki international roaming service is waqt OFF ha. 
Ap k account me koi international roaming minutes, SMS ya data bundle ni ha. """

user1_response = """Ap ye add-on offers subscribe kar sakty hain:\n
Call: Haftawar-Sahulat-Offer (price: Rs. 115, validity: 7 days) jis me 1000 On-net aur 70 Off-net minutes hain.\n
SMS: Weekly-Messaging-Offer (price: Rs. 11.95, validity: 7 days) jis me 1200 SMS hain.\n
Internet: Weekly-Plus-Bundle (price: Rs. 120, validity: 7 days) jis me 1500 MB hain."""

user2_response = """Ap ye add-on offers subscribe kar sakty hain:\n
Call: Haftawar-Chappar-Phaar (price: Rs. 88, validity: 7 days) jis me 2000 On-net minutes hain.\n
SMS: Weekly-SMS-Bundle (price: Rs. 15.50, validity: 7 days) jis me 1200 SMS hain.\n
Internet: 4G-Weekly-Bundle (price: Rs. 90, validity: 7 days) jis me 750 MB + 500MB (WhatsApp) hain."""

utter_user_not_found = "Sorry, mobile number '{mobile_number}' k lye koi record nhi mila"

single_user_object = {
        "user_id": 1,
        "name": "Khalid",
        "user_type": "prepaid",
        "current_package": "Freedom1500",
        "balance": 550,
        "balance_validity": "31-12-2019",
        "remaining_sms": 10000,
        "remaining_onnet": "unlimited",
        "remaining_offnet": 530,
        "remaining_data": 16000,
        "last_recharge": "15-09-2019 ko Rs. 1000",
        "balance_usage": "Ap ab tak Rs.630 ka balance use chuky hain.",
        "emergency_laon_last_availed": "You availed emergency loan on 10-09-2019, returned on 15-09-2019.",
        "roaming_status": "off",
        "roaming-offers": roaming_offers_available,
        "add-on-offers": user1_response,
        "packages_validity": """Ap k resouces ki expiry data ye ha: 10000 SMS (validity: 15-12-2019),
    unlimited Onnet & 530 Offnet minutes (validity: 15-12-2019) and 16000 MB data (validity: 15-12-2019)"""
    }


user_data = {
    "923401111111": single_user_object,
    "923411111111": single_user_object,
    "923421111111": single_user_object,
    "923431111111": single_user_object,
    "923441111111": single_user_object,
    "923451111111": single_user_object,
    "923461111111": single_user_object,
    "923471111111": single_user_object,
    "923481111111": single_user_object,
    "923491111111": single_user_object,
    "923401234567": single_user_object,
    "923411234567": single_user_object,
    "923421234567": single_user_object,
    "923431234567": single_user_object,
    "923441234567": single_user_object,
    "923451234567": single_user_object,
    "923461234567": single_user_object,
    "923471234567": single_user_object,
    "923481234567": single_user_object,
    "923491234567": single_user_object
}


def mobile_verified(mobile_number):
    if mobile_number not in user_data.keys():
        return False, "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)
    return True, user_data[mobile_number]


def get_user_name(mobile_number):
    if mobile_number not in user_data.keys():
        return False
    return user_data[mobile_number]['name']


def get_remaining_balance(mobile_number):
    if mobile_number not in user_data.keys():
        return "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)

    return """Ap ka maujoda balance: Rs. {balance}, validity: {balance_validity}""".format(
        balance=user_data[mobile_number]['balance'],
        balance_validity=user_data[mobile_number]['balance_validity'])


def get_balance_expiry(mobile_number):
    if mobile_number not in user_data.keys():
        return "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)

    return """Ap ka balance khatam hony ki akhri tareekh: {balance_validity}""".format(
        balance_validity=user_data[mobile_number]['balance_validity'])


def get_current_package_information(mobile_number):
    current_package_name = user_data[mobile_number]['current_package']
    current_package_info = combo_packages[current_package_name]
    if mobile_number not in user_data.keys():
        return "No Record Found against mobile_number: {}".format(mobile_number)

    return """Ap ka maujoda package {current_package} ha.
Ap k package me {total_sms} SMS thy, baqi SMS {remaining_sms} hain.
Ap k package me {total_onnet} On-Net minutes thy, baqi minutes {remaining_onnet} hain.
Ap k package me {total_offnet} Off-Net minutes thy, baqi minutes {remaining_offnet} hain.
Ap k package me {total_data} MBs internet thy, baqi MBs {remaining_data} hain.""".format(
        current_package=current_package_name,
        total_sms=current_package_info['sms'],
        remaining_sms=user_data[mobile_number]['remaining_sms'],
        total_onnet=current_package_info['onnet'],
        remaining_onnet=user_data[mobile_number]['remaining_onnet'],
        total_offnet=current_package_info['offnet'],
        remaining_offnet=user_data[mobile_number]['remaining_offnet'],
        total_data=current_package_info['data'],
        remaining_data=user_data[mobile_number]['remaining_data']
    )


def get_last_recharge_info(mobile_number):
    return """Pichli bar ap ny {last_recharge} ka recharge karwaya tha.\n
    AP ka maujoda balance Rs. {balance} ha, validity {balance_validity}""".format(
        last_recharge=user_data[mobile_number]['last_recharge'],
        balance=user_data[mobile_number]['balance'],
        balance_validity=user_data[mobile_number]['balance_validity']
    )


def get_last_recharge_date(mobile_number):
    return """Pichli bar ap ny {last_recharge} ka recharge karwaya tha.""".format(
        last_recharge=user_data[mobile_number]['last_recharge'])


def verify_current_resources(mobile_number):
    if mobile_number not in user_data.keys():
        return "No Record Found against mobile_number: {}".format(mobile_number)

    return """Your current resources are:
Current balance is Rs {balance} with validity upto {balance_validity}.
You have {remaining_sms} SMS remaining.
You have {remaining_onnet} on-net minutes remaining.
You have {remaining_offnet} off-net minutes remaining.
You have {remaining_data} MBs remaining""".format(
        balance=user_data[mobile_number]['balance'],
        balance_validity=user_data[mobile_number]['balance_validity'],
        remaining_sms=user_data[mobile_number]['remaining_sms'],
        remaining_onnet=user_data[mobile_number]['remaining_onnet'],
        remaining_offnet=user_data[mobile_number]['remaining_offnet'],
        remaining_data=user_data[mobile_number]['remaining_data']
    )


def list_all_available_offers(mobile_number):
    if mobile_number not in user_data.keys():
        return "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)
    return user_data[mobile_number]["add-on-offers"]


def get_international_roaming_status(mobile_number):
    roaming_status = user_data[mobile_number]['roaming_status']
    if roaming_status == "on":
        response = active_roaming_response
    else:
        response = non_active_roaming_response
    return response


def list_all_roaming_offers(mobile_number):
    if mobile_number not in user_data.keys():
        return "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)
    return user_data[mobile_number]["roaming-offers"]


def get_packages_validity(mobile_number):
    if mobile_number not in user_data.keys():
        return "Sorry, Is mobile number k lye koi record nhi mila: {}".format(mobile_number)
    return user_data[mobile_number]["packages_validity"]


##########################
# EMERGENCY LOAN
###########################
def get_last_loan_details(mobile_number):
    if mobile_number not in user_data.keys():
        return utter_user_not_found.format(mobile_number=mobile_number)
    return user_data[mobile_number]["emergency_laon_last_availed"]


def get_emergency_loan_status(mobile_number):
    if mobile_number not in user_data.keys():
        return utter_user_not_found.format(mobile_number=mobile_number)
    if not user_data[mobile_number]["emergency_loan_currently_availing"]:
        return "Ap ne emergency loan subscribe nhi kia. Abi Rs.20 ka Loan leny k lye 'YES' likhy."
    return "Sorry, ap ne pichla emergency loan wapis nhi kia abi. Ap mazeed loan nhi hasil kr sakty!"


def set_loan_subscription(mobile_number):
    if mobile_number not in user_data.keys():
        return utter_user_not_found.format(mobile_number=mobile_number)
    if user_data[mobile_number]["emergency_loan_currently_availing"]:
        return "Sorry, ap ne pichla emergency loan wapis nhi kia abi. Ap mazeed loan nhi hasil kr sakty!"
    user_data[mobile_number]["emergency_loan_currently_availing"] = True
    return "Ap ne kamyabi sy Rs.20. ka emergency loan hasil kr lia ha."
