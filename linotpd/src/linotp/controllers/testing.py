# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2015 LSE Leading Security Experts GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@lsexperts.de
#    Contact: www.linotp.org
#    Support: www.lsexperts.de
#
"""
testing controller - for testing purposes
"""



import logging

from pylons import request, response
from linotp.lib.base import BaseController

from linotp.lib.util import  getParam
from linotp.lib.user import  getUserFromParam

from linotp.lib.reply import sendResult, sendError

from linotp.model.meta import Session
from linotp.lib.selftest import isSelfTest
from linotp.lib.policy import get_auth_AutoSMSPolicy

import traceback
from linotp.lib.crypt import urandom

optional = True
required = False

log = logging.getLogger(__name__)

#from paste.debug.profile import profile_decorator

# some twilio like test data
twilio_ok = """<?xml version='1.0' encoding='UTF-8'?>\
<TwilioResponse>\
<Message>\
<Sid>SM6552db38d10548cd4161826fa5754530</Sid>\
<DateCreated>Mon,10 Aug 2015 08:43:33 +0000</DateCreated>\
<DateUpdated>Mon, 10 Aug 2015 08:43:33+0000</DateUpdated>\
<DateSent/>\
<AccountSid>AC710548cd4161826fa5754530ea71fb03</AccountSid>\
<To>+491171410210</To>\
<From>+4911714102109</From><Body>testmessage</Body>\
<Status>queued</Status><NumSegments>1</NumSegments><NumMedia>0</NumMedia>\
<Direction>outbound-api</Direction><ApiVersion>2010-04-01</ApiVersion>\
<Price/>\
<PriceUnit>USD</PriceUnit><ErrorCode/><ErrorMessage/>\
<Uri>/2010-04-01/Accounts/AC710548cd4161826fa5754530ea71fb03/Messages/SM65af\
852db38d10548cd4161826fa5754</Uri>\
<SubresourceUris>\
<Media>/2010-04-01/Accounts/AC710548cd4161826fa5754530ea71fb03/Messages/SM65af\
852db38d10548cd4161826fa5754/Media</Media>\
</SubresourceUris>\
</Message>\
</TwilioResponse>\
"""
twilio_fail = """<?xml version='1.0' encoding='UTF-8'?>\
<TwilioResponse>\
<RestException>\
<Code>21603</Code>\
<Message>A 'From' phone number is required.</Message>\
<MoreInfo>https://www.twilio.com/docs/errors/21603</MoreInfo>\
<Status>400</Status>\
</RestException>\
</TwilioResponse>\
"""


class TestingController(BaseController):

    '''
    The linotp.controllers are the implementation of the web-API to talk to the LinOTP server.

        https://server/testing/<functionname>

    The functions are described below in more detail.
    '''

    def __before__(self):
        return response


    def __after__(self):
        return response


    def autosms(self):
        '''
        This function is used to test the autosms policy

        method:
            testing/autosms

        arguments:
            user    - username / loginname
            realm   - additional realm to match the user to a useridresolver


        returns:
            JSON response
        '''
        log.debug('[autosms]')

        param = request.params
        try:

            if isSelfTest() == False:
                Session.rollback()
                return sendError(response, "The testing controller can only be used in SelfTest mode!", 0)

            user = getUserFromParam(param, required)
            ok = get_auth_AutoSMSPolicy()

            Session.commit()
            return sendResult(response, ok, 0)

        except Exception as e:
            log.exception("[autosms] validate/check failed: %r", e)
            Session.rollback()
            return sendError(response, "validate/check failed:" + unicode(e), 0)

        finally:
            Session.close()
            log.debug('[autosms] done')


    def http2sms(self):
        '''
        This function simulates an HTTP SMS Gateway.

        method:
            test/http2sms

        arguments:

           * sender, absender
           * from, von
           * destination, ziel
           * password, passwort
           * from, von
           * text
           * account
           * api_id


        returns:
           As this is a test controller, the response depends on the input values.

            account = 5vor12, sender = legit
                -> Response Success: "200" (Text)

            account = 5vor12, sender = <!legit>
                -> Response Failed: "Failed" (Text)

            account = clickatel, username = legit
                -> Response Success: "ID <Random Number>" (Text)

            account = clickatel, username = <!legit>
                -> Response Success: "FAILED" (Text)
        '''
        log.debug('[http2sms]')
        param = {}

        try:
            param.update(request.params)

            account = getParam(param, "account", optional=False)
            sender = getParam(param, "sender", optional=True)
            username = getParam(param, "username", optional=True)

            destination = getParam(param, "destination")
            if not destination:
                destination = getParam(param, "ziel")

            text = getParam(param, "text")
            if not text:
                text = getParam(param, "text")

            if not destination:
                raise Exception("Missing <destination>")

            if not text:
                raise Exception("Missing <text>")

            if account == "5vor12":
                if sender == "legit":
                    return "200"
                else:
                    return "Failed"

            elif account == "clickatel":
                if username == "legit":
                    return "ID %i" % int(urandom.randint(1000))
                else:
                    return "FAILED"

            elif account == "twilio":
                if username == "legit":
                    return twilio_ok
                else:
                    return twilio_fail

            Session.commit()
            return "Missing account info."

        except Exception as e:
            log.exception('[http2sms] %r' % e)
            Session.rollback()
            return sendError(response, unicode(e), 0)

        finally:
            Session.close()
            log.debug('[http2sms] done')


#eof###########################################################################

