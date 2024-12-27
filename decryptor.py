import subprocess
import configparser

def decrypt(encrypted, key):
    result = subprocess.check_output(['Encryptor.exe', 'decrypt', encrypted, key])
    return result.decode()

def encrypt(text, key):
    result = subprocess.check_output(['Encryptor.exe', 'encrypt', text, key])
    return result.decode()

default_key = "RemoteOneKeyInstall"
setting = configparser.ConfigParser()
setting.read('Roki.setting')

en = decrypt(setting['chd']['en'], default_key)
print("en:", en)
AdmPwd = decrypt(setting['Roki']['AdmPwd'], en)
print("AdmPwd:", AdmPwd)

en = input("Change en(AdminPanel Password) to ")
en_encrypted = encrypt(en, default_key)
print(en_encrypted)
AdmPwd = input("Change Administrator password to ")
AdmPwd_encrypted = encrypt(AdmPwd, en)
print(AdmPwd_encrypted)

setting['Roki']['AdmPwd'] = AdmPwd_encrypted
setting['chd']['en'] = en_encrypted

with open('Roki.setting', 'w') as configfile:    # save
    setting.write(configfile)
