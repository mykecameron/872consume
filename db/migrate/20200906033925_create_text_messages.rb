class CreateTextMessages < ActiveRecord::Migration[6.0]
  def change
    create_table :text_messages, id: :uuid do |t|
      t.string :from
      t.string :to
      t.string :body

      t.text :raw

      t.timestamps
    end
  end
end
