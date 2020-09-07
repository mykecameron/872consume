ActiveAdmin.register TextMessage do
  permit_params :from, :to, :body

  form do |f|
    f.semantic_errors
    f.inputs do
      f.input :from, as: :hidden, input_html: { value: '8722667863' }
      f.input :to, input_html: { maxlength: 10 }

      f.input :body, as: :text
    end
    f.actions
  end

  show do
    panel "Text Message Details" do

      attributes_table_for text_message do
        [:from, :to, :body, :raw, :created_at, :updated_at, :sent, :error].each do |attr|
          row attr
        end
      end

      active_admin_comments
    end
  end

  member_action :send_text, method: :put do
    Phone::Dialer.new.send_text_message(resource)
    flash[:notice] = 'Successfully sent text message!'
    redirect_to :action => :index
  rescue Phone::Error => e
    flash[:error] = "There was an error sending the text message: #{e.error_message}"
    redirect_to :action => :show
  end

  action_item :send_text_message, only: :show do
    url = admin_text_message_path(text_message) + "/send_text"
    link_to 'Send Text Message', url,
      method: :put,
      class: if text_message.sent?
        'disabled'
      end
  end
end
