class RecoveryMailer < ApplicationMailer
  def recovery_email(email)
    mail(to: email, subject: 'Flag')
  end
end
