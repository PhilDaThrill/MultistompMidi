# coding: utf-8
import mido
import time
print("Setting up Multistomp USB MIDI out")
ioport = mido.open_ioport('ZOOM MS Series MIDI 1') # open USB port
p = mido.Parser()

#This fills up a binary String with 0's (thus nor altering its values), so that the number of characters after the "0b" is the same as "nbr_of_characters"
def getbits(binary_string, nbr_of_bits):
    bitlist=[]
    for i in range(2, len(binary_string)):
        bitlist.append(int(binary_string[i]))
    while len(bitlist) < nbr_of_bits:
        bitlist.insert(0, 0)        
    return bitlist

def int_list_to_hex_list(int_list):
    hex_list= []
    for i in range(len(int_list)):
        hex_list.append(hex(int_list[i]))
    return hex_list

def bin_to_int(listofbits):
    a= 0
    for i in range(len(listofbits)):
        a= a + pow(2, len(listofbits) - i - 1)*listofbits[i]
    return a

def replace_bytes(oldbytes, position, new_value):
    newbytes= []
    for i in range(len(oldbytes)):
        if i != position:
            newbytes.append(oldbytes[i])
        else:
            newbytes.append(new_value)
    return newbytes

def replace_bit(data, byte_position, bit_position, new_bit):
    byte0old= getbits(bin(data[byte_position]), 8)
    byte0new= replace_bytes(byte0old, bit_position, new_bit)
    new_data= replace_bytes(data,byte_position,bin_to_int(byte0new))
    return new_data

def get_fx_focus(patchdata):
    return bin_to_int([getbits(bin(patchdata[129]), 8)[7], getbits(bin(patchdata[124]), 8)[4], getbits(bin(patchdata[128]), 8)[1]])
    
def get_number_of_effects(patchdata):
    return bin_to_int([getbits(bin(patchdata[129]), 8)[3], getbits(bin(patchdata[129]), 8)[4], getbits(bin(patchdata[129]), 8)[5]])

def hex_array_to_message(hex_array):
    p.feed(hex_array)
    p.pending
    return p.get_message()

def flush_ioport():    
    for msg in ioport.iter_pending():
        #print(msg)
        pass

def close_ioport():
    ioport.close()

def send_message(message):
    flush_ioport()
    ioport.send(message)
    
def send_hex_message(hex_message):
    send_message(hex_array_to_message(hex_message))
    
def receive_patch_message():
    data= []
    timeout = 500
    initial_time = time.time() * 1000
    while len(data) < 144 and ((time.time() * 1000 - initial_time) < timeout):
        msgin= ioport.poll() # .receive() # .poll()
        if msgin is not None:
            data= msgin.data
    return data

def receive_bank_message():
    data= []
    timeout = 500
    initial_time = time.time() * 1000
    while ((time.time() * 1000 - initial_time) < timeout):
        msgin= ioport.poll() # .receive() # .poll()
        if msgin is not None and hasattr(msgin, 'program'):
            return msgin.program

