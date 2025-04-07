import re

# NOP
pattern_nop = r"^NOP$"

# MOV
pattern_mov_ab = r"^MOV A,B$"
pattern_mov_ba = r"^MOV B,A$"
pattern_mov_alit = r"^MOV A,-?\d+$"  
pattern_mov_blit = r"^MOV B,-?\d+$"   
pattern_mov_adir = r"^MOV A,\(-?\d+\)$"  ###
pattern_mov_bdir = r"^MOV B,\(-?\d+\)$"  ###
pattern_mov_dir_a = r"^MOV \(-?\d+\),A$" ###
pattern_mov_dir_b = r"^MOV \(-?\d+\),B$" ###

#pattern_mov_alit_especial = r"^MOV A,\d+[bdh]$" ###
pattern_mov_alit_especial = r"^MOV A,[0-9A-F]+[bdh]$" ###
pattern_mov_adir_especial = r"^MOV A,\(\d+[bdh]\)$" ###
pattern_mov_bdir_especial = r"^MOV B,\(\d+[bdh]\)$"  ###
pattern_mov_dir_a_especial = r"^MOV \(\d+[bdh]\),A$" ###
pattern_mov_dir_b_especial = r"^MOV \(\d+[bdh]\),B$" ###

# Casos donde se trata el nombre de una variable sin parentesis
# Como por ejemplo MOV A, nombrevariable1
#pattern_mov_a_variable = r"^MOV A,[A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*$"
#pattern_mov_b_variable = r"^MOV B,[A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*$"

pattern_mov_parb_lit = r"^MOV \(B\),-?\d+$"
## REVISAR (NO ESTOY SEGURO DE QUE ESTE VAYA CON EL PATTERN_MOV_PARB_LIT_ESPECIAL)
pattern_mov_parb_lit_especial = r"^MOV \(B\),\d+[hdb]$"


# ADD
pattern_add_ab = r"^ADD A,B$"
pattern_add_ba = r"^ADD B,A$"
pattern_add_alit = r"^ADD A,-?\d+$" 
pattern_add_blit = r"^ADD B,-?\d+$"
pattern_add_adir = r"^ADD A,\(-?\d+\)$" ###
pattern_add_bdir = r"^ADD B,\(-?\d+\)$" ###
pattern_add_dir = r"^ADD \(-?\d+\)$"    ###

pattern_add_adir_especial = r"^ADD A,\(\d+[bdh]\)$" ###
pattern_add_bdir_especial = r"^ADD B,\(\d+[bdh]\)$" ###
pattern_add_dir_especial = r"^ADD \(\d+[bdh]\)$"    ###

# SUB
pattern_sub_ab = r"^SUB A,B$"
pattern_sub_ba = r"^SUB B,A$"
pattern_sub_alit = r"^SUB A,-?\d+$"
pattern_sub_blit = r"^SUB B,-?\d+$"
pattern_sub_adir = r"^SUB A,\(-?\d+\)$" ###
pattern_sub_bdir = r"^SUB B,\(-?\d+\)$" ###
pattern_sub_dir = r"^SUB \(-?\d+\)$"    ###

pattern_sub_adir_especial = r"^SUB A,\(\d+[bdh]\)$" ###
pattern_sub_bdir_especial = r"^SUB B,\(\d+[bdh]\)$" ###
pattern_sub_dir_especial = r"^SUB \(\d+[bdh]\)$"    ###

# AND
pattern_and_ab = r"^AND A,B$"
pattern_and_ba = r"^AND B,A$"
pattern_and_alit = r"^AND A,-?\d+$"
pattern_and_blit = r"^AND B,-?\d+$"
pattern_and_adir = r"^AND A,\(-?\d+\)$" ###
pattern_and_bdir = r"^AND B,\(-?\d+\)$" ###
pattern_and_dir = r"^AND \(-?\d+\)$"    ###

pattern_and_adir_especial = r"^AND A,\(\d+[bdh]\)$" ###
pattern_and_bdir_especial = r"^^AND B,\(\d+[bdh]\)$" ###
pattern_and_dir_especial = r"^AND \(\d+[bdh]\)$"    ###


# OR
pattern_or_ab = r"^OR A,B$"
pattern_or_ba = r"^OR B,A$"
pattern_or_alit = r"^OR A,-?\d+$"
pattern_or_blit = r"^OR B,-?\d+$"
pattern_or_adir = r"^OR A,\(-?\d+\)$"  ###
pattern_or_bdir = r"^OR B,\(-?\d+\)$"  ###
pattern_or_dir = r"^OR \(-?\d+\)$"     ###

pattern_or_adir_especial = r"^OR A,\(\d+[bdh]\)$"  ###
pattern_or_bdir_especial = r"^OR B,\(\d+[bdh]\)$"  ###
pattern_or_dir_especial = r"^OR \(\d+[bdh]\)$"     ###

# XOR
pattern_xor_ab = r"^XOR A,B$"
pattern_xor_ba = r"^XOR B,A$"
pattern_xor_alit = r"^XOR A,-?\d+$"
pattern_xor_blit = r"^XOR B,-?\d+$"
pattern_xor_adir = r"^XOR A,\(-?\d+\)$" ###
pattern_xor_bdir = r"^XOR B,\(-?\d+\)$" ###
pattern_xor_dir = r"^XOR \(-?\d+\)$"    ###

pattern_xor_adir_especial = r"^XOR A,\(\d+[bdh]\)$" ###
pattern_xor_bdir_especial = r"^XOR B,\(\d+[bdh]\)$" ###
pattern_xor_dir_especial = r"^XOR \(\d+[bdh]\)$"    ###

# NOT
pattern_not_a = r"^NOT A$"
pattern_not_ba = r"^NOT B,A$"
pattern_not_dir_a = r"^NOT \(-?\d+\),A$" ###
### FALTA LA INSTRUCCION (B), A PARA NOT SHL SHR #####

pattern_not_dir_a_especial = r"^NOT \(\d+[bdh]\),A$" ###


# SHL
pattern_shl_a = r"^SHL A$"
pattern_shl_ba = r"^SHL B,A$"
pattern_shl_dir_a = r"^SHL \(-?\d+\),A$"  ###
### FALTA LA INSTRUCCION (B), A PARA NOT SHL SHR

pattern_shl_dir_a_especial = r"^SHL \(\d+[bdh]\),A$" ###

# SHR
pattern_shr_a = r"^SHR A$"
pattern_shr_ba = r"^SHR B,A$"
pattern_shr_dir_a = r"^SHR \(-?\d+\),A$" ###
### FALTA LA INSTRUCCION (B), A PARA NOT SHL SHR

pattern_shr_dir_a_especial = r"^SHR \(\d+[bdh]\),A$"

# INC
pattern_inc_a = r"^INC A$"
pattern_inc_b = r"^INC B$"
pattern_inc_dir = r"^INC \(-?\d+\)$" ###

pattern_inc_dir_especial = r"^INC \(\d+[bdh]\)$" ###

# DEC
pattern_dec_a = r"^DEC A$"

# CMP
pattern_cmp_ab = r"^CMP A,B$"
pattern_cmp_alit = r"^CMP A,-?\d+$"
pattern_cmp_adir = r"^CMP A,\(-?\d+\)$"

pattern_cmp_adir_especial = r"^CMP A,\(\d+[bdh]\)$"

pattern_cmp_a_parb = r"^CMP A,\(B\)$"

# JUMPs
pattern_jmp_dir = r"^JMP -?\d+$"
pattern_jeq_dir = r"^JEQ -?\d+$"
pattern_jne_dir = r"^JNE -?\d+$"
pattern_jgt_dir = r"^JGT -?\d+$"
pattern_jge_dir = r"^JGE -?\d+$"
pattern_jlt_dir = r"^JLT -?\d+$"
pattern_jle_dir = r"^JLE -?\d+$"
pattern_jcr_dir = r"^JCR -?\d+$"

#CALL
pattern_call = r"^CALL -?\d+$"

