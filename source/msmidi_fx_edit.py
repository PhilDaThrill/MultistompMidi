# coding: utf-8
import mido
import ms_utils

def go_editor_mode():
    go_editor_mode_hex_array= [0xf0,0x52,0x00,0x61,0x50,0xf7]
    ms_utils.send_hex_message(go_editor_mode_hex_array)

go_editor_mode()

def switch_patch(patch_nbr):
    program_change = mido.Message('program_change', program = patch_nbr)
    ms_utils.send_message(program_change)
    
def edit_parameter(fx_nbr, param_nbr, value):
    bits= ms_utils.getbits(bin(value), 16)
    msbits= []
    lsbits= []
    for i in range(8):
        msbits.append(bits[i])
    for i in range(8):
        lsbits.append(bits[i + 8])
    parameter_data_hexarray = [0xf0,0x52,0x00,0x61,0x31,fx_nbr, param_nbr, ms_utils.bin_to_int(lsbits), ms_utils.bin_to_int(msbits), 0xf7]
    ms_utils.send_hex_message(parameter_data_hexarray)

def retrieve_patch_data():
    request_patch_hex_array= [0xf0,0x52,0x00,0x61,0x29,0xf7]
    ms_utils.send_hex_message(request_patch_hex_array)
    patchdata= ms_utils.receive_patch_message()
    return patchdata

def retrieve_program_number():
    request_bank_hex_array= [0xf0,0x52,0x00,0x61,0x33,0xf7]
    ms_utils.send_hex_message(request_bank_hex_array)
    program_number = ms_utils.receive_bank_message()
    return program_number
 
def retrieve_number_of_effects():
    return ms_utils.get_number_of_effects(retrieve_patch_data())

def switch_fx(switch_step):
    patchdata= retrieve_patch_data()
    fx_focus= ms_utils.get_fx_focus(patchdata)
    number_of_fx= ms_utils.get_number_of_effects(patchdata)
    nrm_fx_focus= fx_focus - (6 - number_of_fx) #normalized fx focus means that the fx furthest to the left is always at slot 0.
    pot_nrm_fx_focus= nrm_fx_focus + switch_step    
    if pot_nrm_fx_focus >= 0 and pot_nrm_fx_focus < number_of_fx:
        #print("...Switching FX from ", nrm_fx_focus, " to ", pot_nrm_fx_focus)
        pot_fx_focus= pot_nrm_fx_focus + 6 - number_of_fx
        pot_fx_focus_bin= ms_utils.getbits(bin(pot_fx_focus), 8)
        newpatchdata= ms_utils.replace_bit(patchdata, 128, 1, pot_fx_focus_bin[7])
        newpatchdata= ms_utils.replace_bit(newpatchdata, 124, 4, pot_fx_focus_bin[6])
        newpatchdata= ms_utils.replace_bit(newpatchdata, 129, 7, pot_fx_focus_bin[5])
        new_patch_message= mido.Message('sysex', data=newpatchdata)
        ms_utils.send_message(new_patch_message)
        return 1
    else:
        return 0
 
def get_tap_tempo():
    patchdata_tt= retrieve_patch_data()
    tap_tempo = 0
    tap_tempo = tap_tempo + 1 * ms_utils.getbits(bin(patchdata_tt[129]), 8)[2]
    tap_tempo = tap_tempo + 2 * ms_utils.getbits(bin(patchdata_tt[129]), 8)[1]
    tap_tempo = tap_tempo + 4 * ms_utils.getbits(bin(patchdata_tt[124]), 8)[5]
    tap_tempo = tap_tempo + 8 * ms_utils.getbits(bin(patchdata_tt[130]), 8)[7]
    tap_tempo = tap_tempo + 16 * ms_utils.getbits(bin(patchdata_tt[130]), 8)[6]
    tap_tempo = tap_tempo + 32 * ms_utils.getbits(bin(patchdata_tt[130]), 8)[5]
    tap_tempo = tap_tempo + 64 * ms_utils.getbits(bin(patchdata_tt[130]), 8)[4]
    tap_tempo = tap_tempo + 128 * ms_utils.getbits(bin(patchdata_tt[130]), 8)[3]
    return tap_tempo
 
def set_tap_tempo(tap_tempo):
    #Note: Any tempo set below 40 or above 250 would not work on the Multistomp, but set it to 120.
    patchdata_tt= retrieve_patch_data()
    tap_tempo_bin= ms_utils.getbits(bin(tap_tempo), 8)
    newpatchdata_tt= ms_utils.replace_bit(patchdata_tt, 129, 2, tap_tempo_bin[7])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 129, 1, tap_tempo_bin[6])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 124, 5, tap_tempo_bin[5])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 130, 7, tap_tempo_bin[4])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 130, 6, tap_tempo_bin[3])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 130, 5, tap_tempo_bin[2])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 130, 4, tap_tempo_bin[1])
    newpatchdata_tt= ms_utils.replace_bit(newpatchdata_tt, 130, 3, tap_tempo_bin[0])    
    new_patch_message= mido.Message('sysex', data=newpatchdata_tt)
    ms_utils.send_message(new_patch_message)

def leave_editor_mode():
    leave_editor_mode_hex_message= [0xf0,0x52,0x00,0x61,0x51,0xf7]
    ms_utils.send_hex_message(leave_editor_mode_hex_message)

def wrap_up():
    leave_editor_mode()
    print("Done.")
