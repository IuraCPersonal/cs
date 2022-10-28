require_relative 'ciphers/block/des'
require_relative 'ciphers/stream/rc4'

key = "fcim faf"
text = "software-engineer"

rc4_enc = RC4.new(key)
encrypted = rc4_enc.encrypt(text)

puts "Original text: #{text}"
puts "Key: #{key}"
p "RC4 Encrypted: #{encrypted}"


data = RubyDES::Block.new('mysecret')
key  = RubyDES::Block.new('hushhush')

des = RubyDES::Ctx.new(data, key)

encrypted_data = des.encrypt.bit_array.join

puts "Original text: mysecret"
puts "Key: hushhush"
p "DES Encrypted: #{encrypted_data}"
