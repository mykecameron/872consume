class TwilioWebhooks::SmsController < ApplicationController
  def create
    twiml = Twilio::TwiML::Response.new do |r|
      r.Message 'The Robots are coming! Head for the hills!'
    end

    render xml: twiml.text
  end
end
