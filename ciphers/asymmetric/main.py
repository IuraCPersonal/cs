import time
import streamlit as st 
from rsa_cipher import RSA
from rsa_key_gen import RSA_KEY_GEN

st.title("RSA (Rivest–Shamir–Adleman)")

st.write("""RSA (Rivest–Shamir–Adleman) is a public-key cryptosystem that 
        is widely used for secure data transmission. In a public-key cryptosystem, 
        the encryption key is public and distinct from the decryption key, which is 
        kept secret (private). An RSA user creates and publishes a public key based 
        on two large prime numbers, along with an auxiliary value. The prime numbers 
        are kept secret. Messages can be encrypted by anyone, via the public key, but 
        can only be decoded by someone who knows the prime numbers.""")

st.header("How it works?")

with st.form('user_inputs'):
    key_size = st.number_input('Enter Key Size...', min_value=0, step=1, value=1024)
    block_size = st.number_input('Enter Block Size...', step=1, value=128)

    message = st.text_input('Enter Message...')

    submited = st.form_submit_button()

if submited:
    public_key, private_key = RSA_KEY_GEN.key_gen(key_size)

    st.subheader("Generating Public Key (n, e)")

    time.sleep(2)
    st.write(public_key)

    st.subheader("Generate Private Key (n, d)")

    time.sleep(2)
    st.write(private_key)

    rsa = RSA(message)
    encrypted = rsa.encrypt(public_key, block_size)
    st.subheader("Encrypting...")
    time.sleep(2)
    st.write(encrypted[0])

st.header("Decrypt your message")

with st.form('user_inputs_2'):
    encrypted_message = [int(x) for x in st.text_input('Enter Encrypted Message...').split()]
    message_length = st.number_input('Enter Message Length...', min_value=0, step=1)
    str_private_key = st.text_input('Enter Private Key...')
    private_key = [int(x) for x in str_private_key.split()]

    submited_decrypt = st.form_submit_button()

if submited_decrypt:
    rsa = RSA(None)
    decrypted = rsa.decrypt(encrypted_message, message_length, private_key, message_length)
    st.write(decrypted)