require 'rails_helper'

RSpec.describe "Calls", type: :request do
  describe "GET /index" do
    it "responds with 'hello world' in TwiML" do
      post '/calls'

      expect(response.content_type).to eql 'application/xml; charset=utf-8'
      expect(response.body).to eql "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n<Say>Hello World</Say>\n</Response>\n"
    end
  end
end
