class TextMessage < ApplicationRecord
  PHONE_NUMBER_FORMAT = {
    with: /\d{10}/,
    message: "must be 10 digits"
  }

  validates :to,   presence: true, format: PHONE_NUMBER_FORMAT
  validates :from, presence: true, format: PHONE_NUMBER_FORMAT
  validates :body, presence: true

end
