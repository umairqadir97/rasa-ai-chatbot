
## agent.can_you_help
* agent.can_you_help
    - utter_agent.can_you_help

## agent.good
* agent.good
    - utter_agent.good

## agent.happy
* agent.happy
    - utter_agent.happy  

## agent.there
* agent.there
    - utter_agent.there

## appraisal.good
* appraisal.good
    - utter_appraisal.good
  
## appraisal.no_problem
* appraisal.no_problem
    - utter_appraisal.no_problem

## appraisal.thank_you
* appraisal.thank_you
    - utter_appraisal.thank_you

## appraisal.welcome
* appraisal.welcome
    - utter_appraisal.welcome

## confirmation.no
* confirmation.no
    - utter_confirmation.no

## confirmation.yes
* confirmation.yes
    - utter_confirmation.yes

## dialog.sorry
* dialog.sorry
    - utter_dialog.sorry

## greetings.bye
* greetings.bye
    - utter_greetings.bye 

## greetings.goodevening
* greetings.goodevening
    - utter_greetings.goodevening

## greetings.goodmorning
* greetings.goodmorning
    - utter_greetings.goodmorning    
 
## greetings.goodnight
* greetings.goodnight
    - utter_greetings.goodnight

## greetings.hello -- verified users
* greetings.hello
    - slot{"verification" : "yes"}
    - action_hello_user

## greetings.hello -- without verification
* greetings.hello
    - slot{"verification" : "no"}
    - utter_greetings.hello


## greetings.how_are_you
* greetings.how_are_you
    - utter_greetings.how_are_you
    

## greetings.nice_to_meet_you
* greetings.nice_to_meet_you
    - utter_greetings.nice_to_meet_you

## greetings.nice_to_see_you
* greetings.nice_to_see_you
    - utter_greetings.nice_to_see_you

## greetings.nice_to_talk_to_you
* greetings.nice_to_talk_to_you
    - utter_greetings.nice_to_talk_to_you

## user.excited
* user.excited
    - utter_user.excited

## user.good
* user.good
    - utter_user.good

## user.happy
* user.happy
    - utter_user.happy


## balance.balance_info
* balance.balance_info
    - slot{"verification" : "yes"}
    - action_balance_info
* time_limit
    - slot{"verification" : "yes"}
    - action_balance_expiry


## authentication Required ------------------------ balance_info
* balance.balance_info
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_balance_info
* time_limit
    - slot{"verification" : "yes"}
    - action_balance_expiry


## balance.balance_validity
* balance.balance_validity
    - slot{"verification" : "yes"}
    - action_balance_expiry
* how_much
    - slot{"verification" : "yes"}
    - action_balance_info


## authentication Required -------------------- balance_validity
* balance.balance_validity
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_balance_expiry
* how_much
    - slot{"verification" : "yes"}
    - action_balance_info


## incomplete query: kitna ha, how_muc ?
* how_much
    - utter_incomplete_query


## incomplete query, kab tak rhy ga, time_limit ?
* time_limit
    - utter_incomplete_query


## emergency_loan.general_information -- subscription
* emergency_loan.general_loan_service_info
    - utter_emergency_loan_general_info
* subscribe_above_offer
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.yes
    - slot{"verification" : "yes"}
    - action_emergency_loan_subscribe
    
## authentication Required --------- general_information -- subscription
* emergency_loan.general_loan_service_info
    - utter_emergency_loan_general_info
* subscribe_above_offer
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.yes
    - slot{"verification" : "yes"}
    - action_emergency_loan_subscribe

## emergency_loan.general_information -- interested but no subscription
* emergency_loan.general_loan_service_info
    - slot{"verification" : "yes"}
    - utter_emergency_loan_general_info
* subscribe_above_offer
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.no
    - slot{"verification" : "yes"}
    - utter_confirmation.no
    
    
## authentication Required ------- general_information, no subscription
* emergency_loan.general_loan_service_info
    - utter_emergency_loan_general_info
* subscribe_above_offer
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.no
    - slot{"verification" : "yes"}
    - utter_confirmation.no
    
    
## emergency_loan_status -- subscription
* emergency_loan.current_status
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.yes
    - slot{"verification" : "yes"}
    - action_emergency_loan_subscribe
    
## authentication Required --------------- emergency_loan.current_status
* emergency_loan.current_status
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.yes
    - slot{"verification" : "yes"}
    - action_emergency_loan_subscribe


## emergency_loan_status -- (just status)
* emergency_loan.current_status
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.no
    - utter_confirmation.no

## authentication Required ------------------- emergency_loan_status
* emergency_loan.current_status
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_emergency_loan_current_status
* confirmation.no
    - utter_confirmation.no


## emergency_loan.last_availed
* emergency_loan.last_availed
    - slot{"verification" : "yes"}
    - action_emergency_loan_last_availed

## authentication Required ----------------------------- LOAN ends here
* emergency_loan.last_availed
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_emergency_loan_last_availed

## last recharge info
* last_recharge.info
    - slot{"verification" : "yes"}
    - action_last_recharge_info
* when_did_i
    - slot{"verification" : "yes"}
    - action_last_recharge_date

## authentication Required -------------------- Last_Recharge info
* last_recharge.info
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_last_recharge_info
* when_did_i
    - slot{"verification" : "yes"}
    - action_last_recharge_date


## last recharge date
* last_recharge.date
    - slot{"verification" : "yes"}
    - action_last_recharge_date
* how_much
    - slot{"verification" : "yes"}
    - action_last_recharge_info


## authentication Required -------------------- Last_Recharge date
* last_recharge.date
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_last_recharge_date
* how_much
    - slot{"verification" : "yes"}
    - action_last_recharge_info


## balance usage 
* balance.balance_usage
    - slot{"verification" : "yes"}
    - action_balance_usage_report

## authentication Required -------------------- Balance_Usage ends here
* balance.balance_usage
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_balance_usage_report


## offers information -- interested
* offers.info
    - action_offers_info
* confirmation.yes
    - slot{"verification" : "yes"}
    - action_offers_subscribe

## offers information -- not interested
* offers.info
    - action_offers_info
* confirmation.no
    - utter_confirmation.no

## offers information -- thank you not interested
* offers.info
    - action_offers_info
* appraisal.thank_you
    - utter_confirmation.no

## offers information -- authentication failed
* offers.info
    - action_offers_info
* confirmation.yes
    - slot{"verification" : "no"}
    - action_verification_required
    - form{"name": "action_verification_required"}
    - form{"name": null}
    - slot{"verification" : "yes"}
    - action_offers_subscribe


## out_of_scope
* out_of_scope
    - action_custom_fallback