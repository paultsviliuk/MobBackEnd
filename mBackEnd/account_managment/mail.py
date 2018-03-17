import smtplib

smpt_host='smtp.gmail.com'
smpt_port=587

login='suppmob24@gmail.com'
password='4kn-dXz-rBZ-5Wf'

send_from="alan@mail.ru"
password_subject="Password Restore"
password_message="Here is your password.\n Password: "

promo_code_subject="Promo Code"
promo_code_message="Here is your promo code.\n Promo Code: "



def sendPassword(send_to,user_password):
    smtp=smtplib.SMTP(smpt_host,smpt_port)
    smtp.starttls()
    smtp.login(login,password)
    smtp.sendmail(send_from,send_to,password_message+user_password)
    smtp.quit()

def sendPromoCode(send_to,promo_code):
    smtp = smtplib.SMTP(smpt_host, smpt_port)
    smtp.starttls()
    smtp.login(login, password)
    smtp.sendmail(send_from, send_to, promo_code_message + promo_code)
    smtp.quit()