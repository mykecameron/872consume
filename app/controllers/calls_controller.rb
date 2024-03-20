class CallsController < ApplicationController
  skip_forgery_protection only: :create
  
  def create
    response = Twilio::TwiML::VoiceResponse.new do | response |
      response.say(message: "Hello World")
    end

    render xml: response
  end
end
