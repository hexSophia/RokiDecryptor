#include <Crypt.au3>

; Check if the necessary command-line arguments are provided
If $CmdLine[0] < 3 Then
    ConsoleWrite("Usage: script.exe [encrypt|decrypt] data key" & @CRLF)
    Exit
EndIf

; Retrieve command-line arguments
$operation = $CmdLine[1]
$data = $CmdLine[2]
$hkey = $CmdLine[3]

; Perform encryption or decryption based on the operation argument
If $operation = "encrypt" Then
    $result = _rokicrypt_encryptdata($data, $hkey)
    ConsoleWrite($result & "")
ElseIf $operation = "decrypt" Then
    $result = _rokicrypt_decryptdata($data, $hkey)
    ConsoleWrite($result & "")
Else
    ConsoleWrite("Invalid operation. Use 'encrypt' or 'decrypt'." & @CRLF)
    Exit
EndIf

; Encryption function
Func _rokicrypt_encryptdata($data, $hkey)
    _Crypt_Startup()
    Local $g_hkey = _Crypt_DeriveKey(StringToBinary($hkey), $CALG_AES_256)
    Local $encryptedData = _Crypt_EncryptData($data, $g_hkey, $CALG_USERKEY)
    _Crypt_Shutdown()
    Return $encryptedData
EndFunc

; Decryption function
Func _rokicrypt_decryptdata($encryptedData, $hkey)
    _Crypt_Startup()
    Local $g_hkey = _Crypt_DeriveKey(StringToBinary($hkey), $CALG_AES_256)
    Local $decryptedData = _Crypt_DecryptData($encryptedData, $g_hkey, $CALG_USERKEY)
    _Crypt_Shutdown()
    Return BinaryToString($decryptedData)
EndFunc
