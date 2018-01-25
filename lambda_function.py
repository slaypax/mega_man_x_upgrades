from __future__ import print_function
import json

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I can tell you where to find upgrades in Mega Man X. "
    reprompt_text = "Let me know if I can help you find anything " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using mega man upgrades. " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def create_upgrade_attributes(desired_upgrade):
    print("trying to create upgrade attributes")
    str(desired_upgrade)
    print(desired_upgrade)
    return {"desiredUpgrade": desired_upgrade}

def create_stage_attributes(desired_stage):
    print("trying to create upgrade attributes")
    str(desired_stage)
    print(desired_stage)
    return {"desiredStage": desired_stage}

def set_upgrade_in_session(intent, session):

    with open("upgrades.json", 'r') as f:
        upgrades = json.load(f)

    card_title = intent['name']
    session_attributes = {}
   
    should_end_session = False
    if 'Upgrade' in intent['slots']:
        print("took if code path")
        print(intent['slots'])
        try:
            desired_upgrade = intent['slots']['Upgrade']['value']
            print(desired_upgrade)
            session_attributes = create_stage_attributes(desired_upgrade)
            print(session_attributes)
        except KeyError:
            speech_output = "Are you still there? What upgrade do you need help finding?"
            reprompt_text = "You can ask me for the location of an Upgrade by saying where is the followed by the upgrade "
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        try:
            speech_output = upgrades["upgrade locations"][desired_upgrade]
        except KeyError:
            speech_output = "That's not an upgrade. Try asking me where to find the Arm Upgrade, Chest Upgrade, Helmet Upgrade, Leg upgrade, or the Hadouken. "
            reprompt_text = "You can ask me for the location of an Upgrade by saying where is the followed by the upgrade "
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        
        reprompt_text = "You can ask me for the location of an Upgrade by saying where is the followed by the upgrade. I can also tell you where to find Heart Tanks. "
                  
    else:
        print("took else code path")
        print(intent['slots'])
        print(speech_output)
        speech_output = "I'm not sure what upgrade you're looking for. Try again. "
        reprompt_text = speech_output + "You can ask me for the location of an Upgrade by saying where is the followed by the upgrade "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_stage_in_session(intent, session):
    """ 
    used to retrive the location of the heart tank for a given stage name
    """
    with open("upgrades.json", 'r') as f:
        upgrades = json.load(f)

    card_title = intent['name']
    session_attributes = {}
    
    should_end_session = False
    if 'Stage' in intent['slots']:
        print("took if code path")
        print(intent['slots'])
        try:
            desired_stage = intent['slots']['Stage']['value']
            print(desired_stage)
            session_attributes = create_stage_attributes(desired_stage)
            print(session_attributes)
        except KeyError:
            speech_output = "Are you still there? What heart tank do you need help finding?"
            reprompt_text = "There is a heart tank in every stage. You can ask me for the location of a heart tank by saying where is the heart tank in, followed by the stage name"
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        try:
            speech_output = upgrades["heart locations"][desired_stage]
        except KeyError:
            speech_output = "That's not a valid stage name."
            reprompt_text = "You can ask me for the location of a heart tank by saying where is the heart tank in, followed by the stage name"
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        
        reprompt_text = "You can ask me for the location of a heart tank by saying where is the heart tank in, followed by the stage name"
    else:
        print(intent['slots'])
        print(speech_output)
        speech_output = "I'm not sure what upgrade you're looking for. Try again. "
        reprompt_text = speech_output + "You can ask me for the location of an Upgrade by saying where is the followed by the upgrade "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_session_started(session_started_request, session):

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):


    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    return get_welcome_response()


def on_intent(intent_request, session):


    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    print(intent)
    intent_name = intent_request['intent']['name']

    # Dispatch intent handlers
    if intent_name == "MyUpgradeIntent":
        return set_upgrade_in_session(intent, session)
    elif intent_name == "MyHeartTankIntent":
        return set_stage_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def lambda_handler(event, context):

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.a2523332-b568-47fe-918d-639a247cad5a"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
