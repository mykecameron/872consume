module Phone
  def self.client
    @client ||= begin
      account_sid = ENV['TWILIO_SID']
      auth_token = ENV['TWILIO_AUTH_TOKEN']
      Twilio::REST::Client.new account_sid, auth_token
    end
  end

  class Dialer
    def send_text_message(text_message)
      client.messages.create(
        from: "+1#{text_message.from}",
        to:   "+1#{text_message.to}",
        body: text_message.body,
      )

      text_message.sent = true
    rescue Twilio::REST::RestError => e
      text_message.error = e.error_message
      raise Error.new(e.error_message, text_message, e)
    ensure
      text_message.save
    end

    def client
      @client ||= Phone.client
    end
  end

  class Error < StandardError
    attr_reader :error_message, :text_message, :originating_error

    def initialize(error_message, text_message, originating_error)
      self.error_message = error_message
      self.text_message = text_message
      self.originating_error = originating_error
      super(error_message)
    end

    private

    attr_writer :error_message, :text_message, :originating_error
  end
end
