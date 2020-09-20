class AddSentAndErrorToTextMessages < ActiveRecord::Migration[6.0]
  def change
    add_column :text_messages, :sent, :boolean
    add_column :text_messages, :error, :string
  end
end
