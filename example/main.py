# [START app]

import logging

## import the bypass auth pkg with the sms method
import bypass_auth.bypass_sms as bypass_sms
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# [START Launch]
@ask.launch
def new_query():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)
# [END Launch]

# [START 2_factor_auth]
@ask.intent("YesIntent")
def next_round():
    
    #### Add your flowroute number here
    # future, initiate auth service
    to_number = '###-###-####'
    pass_code = bypass_sms.send_auth('###-###-####')
    auth_msg = render_template('auth')
    session.attributes['pass_code'] = pass_code
    return question(auth_msg)
# [END 2_factor_auth]

# [START Launch]
@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int})
def answer(first, second, third, fourth):
    auth_numbers = session.attributes['pass_code']
    name = "Default" ## query your user's name
    # Future pass this to auth service and return session.auth data
    if [first, second, third, fourth] == auth_numbers:
        session.attributes['auth'] = True
        msg = render_template('pass', name=name)
    else:
        msg = render_template('fail')
    return statement(msg)
# [END Launch]

# [START query]
@ask.intent("QueryIntent")
def sf_query():
    # future, query data from SF instance and return payload and success message
    session.attribute['company_data'] = ["company1","company2","company3","company4","company5"]
    success = True
    if success:
        return render_template('query_status_OK')
    else:
        query_status = render_template('query_status_fail')
    return question(query_status)
# [END query]

# [START 2_factor_auth]
@ask.intent("FollowIntent", mapping={'method':'method'})
def say_send():
    # future, initiate auth service
    if method == 'phone' or method == 'device':
        #send it to the phone
        success_msg = render_template('success_phone')
    else:
        company_string = session['company_data'][0]
        for company in session['company_data']:
            company_string += ", "
            company_string += company
        success_msg = render_template('success_say', companies = company_string)
    return question(success_msg)
# [END 2_factor_auth]

# [END app]

if __name__ == '__main__':
    app.run(debug=True)