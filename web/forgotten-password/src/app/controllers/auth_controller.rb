class AuthController < ApplicationController


  def login
  end

  def forget
  end

  def recover
    user_found = false
    User.all.each { |user|
      if params[:email].include?(user.email)
        user_found = true
        break
      end
    }

    if user_found
      RecoveryMailer.recovery_email(params[:email]).deliver_now
      redirect_to forgot_password_path, notice: 'Password reset email sent'
    else
      redirect_to forgot_password_path, alert: 'You are not a registered user!'
    end

  end
end
