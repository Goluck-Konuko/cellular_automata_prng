import numpy as np 
import itertools
import operator
import io
import time


'''
TODO
-Test different update rules
-Test for statistical independence on longer sequences
-Test different initializations
-Test for epsilon soft in rule and mechanism selections.
'''

#First update mechanism
def model_one(x,y,z,rule,automaton):
    if(x<7 and y<7):
        if(x==0 and y==0):
            cell  = rule[0]^rule[1]^(rule[2] and automaton[7,y,z])^(rule[3] and automaton[x+1,y,z])^(rule[4] and automaton[x,7,z])^(rule[5] and automaton[x,y+1,z])
        elif(x==0 and y>0):
            cell  = rule[0]^rule[1]^(rule[2] and automaton[7,y,z])^(rule[3] and automaton[x+1,y,z])^(rule[4] and automaton[x,y-1,z])^(rule[5] and automaton[x,y+1,z])
        elif(y==0 and x>0):
            cell  = rule[0]^rule[1]^(rule[2] and automaton[x,y,z])^(rule[3] and automaton[x+1,y,z])^(rule[4] and automaton[x,7,z])^(rule[5] and automaton[x,y+1,z])
        else:
            cell  = rule[0]^rule[1]^(rule[2] and automaton[x-1,y,z])^(rule[3] and automaton[x+1,y,z])^(rule[4] and automaton[x,y-1,z])^(rule[5] and automaton[x,y+1,z])
    else:
        if(x==7 and y==7):
            cell  = rule[0]^rule[1]^(rule[2] and automaton[x-1,y,z])^(rule[3] and automaton[0,y,z])^(rule[4] and automaton[x,y-1,z])^(rule[5] and automaton[x,0,z])
        elif(x==7 and y<7):
            cell  = rule[0]^rule[1]^(rule[2] and automaton[x-1,y,z])^(rule[3] and automaton[0,y,z])^(rule[4] and automaton[x,y-1,z])^(rule[5] and automaton[x,y+1,z])
        else:
            cell  = rule[0]^rule[1]^(rule[2] and automaton[x-1,y,z])^(rule[3] and automaton[x+1,y,z])^(rule[4] and automaton[x,y-1,z])^(rule[5] and automaton[x,0,z])
    return cell

#second update mechanism
def model_two(x,y,z,rule,automaton):
    if(y<7 and z<7):
        if(y==0 and z==0):
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,7,z]) ^ (rule[5] and automaton[x,y+1,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,7])
        elif(y==0 and z>0):
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,7,z]) ^ (rule[5] and automaton[x,y+1,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
        elif(z==0 and y>0):
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,y-1,z]) ^ (rule[5] and automaton[x,y+1,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,7])
        else:
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,y-1,z]) ^ (rule[5] and automaton[x,y+1,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
    else:
        if(y==7 and z==7):
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,y-1,z]) ^ (rule[5] and automaton[x,0,z]) ^ (rule[6] and automaton[x,y,0]) ^ (rule[7] and automaton[x,y,z-1])
        elif(y==7 and z<7):
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,y-1,z]) ^ (rule[5] and automaton[x,0,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
        else:
            cell = rule[0] ^ rule[1] ^ (rule[4] and automaton[x,y-1,z]) ^ (rule[5] and automaton[x,y+1,z]) ^ (rule[6] and automaton[x,y,0]) ^ (rule[7] and automaton[x,y,z-1])
    return cell

def model_three(x,y,z,rule,automaton):
    if(x<7 and z<7):
        if(x==0 and z==0):
           cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[7,y,z]) ^ (rule[3] and automaton[x+1,y,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,7])
        elif(x==0 and z>0):
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[7,y,z]) ^ (rule[3] and automaton[x+1,y,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
        elif(z==0 and x>0):
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[x-1,y,z]) ^ (rule[3] and automaton[x+1,y,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,7])
        else:
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[x-1,y,z]) ^ (rule[3] and automaton[x+1,y,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
    else:
        if(x==7 and z==7):
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[x-1,y,z]) ^ (rule[3] and automaton[0,y,z]) ^ (rule[6] and automaton[x,y,0]) ^ (rule[7] and automaton[x,y,z-1])
        elif(x==7 and z<7):
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[x-1,y,z]) ^ (rule[3] and automaton[0,y,z]) ^ (rule[6] and automaton[x,y,z+1]) ^ (rule[7] and automaton[x,y,z-1])
        else:
            cell = rule[0] ^ rule[1] ^ (rule[2] and automaton[x-1,y,z]) ^ (rule[3] and automaton[x+1,y,z]) ^ (rule[6] and automaton[x,y,0]) ^ (rule[7] and automaton[x,y,z-1])
    return cell


# Generate a bitstream
def generate(sequences,evolutions):
    bit_sequence = []
    rules = np.array([
        [1, 0, 0, 1, 1, 1, 1, 0], #rule 30
        [0, 1, 1, 1, 1, 1, 1, 0], #rule 110
        [1, 1, 0, 1, 1, 1, 1, 1], #rule 222
        [1, 1, 1, 1, 1, 0, 1, 1], #rule 250
        [0, 0, 1, 0, 1, 0, 1, 1], #rule 43
        [0, 1, 0, 1, 0, 1, 0, 1], #rule 85
        [1, 0, 1, 0, 1, 0, 1, 0], #rule 170
        [1, 1, 0, 0, 1, 0, 0, 1]  #rule 201
        ])
    
    for i in range(sequences):
        automaton = np.random.randint(0,2,(8,8,8)) #intialize a random cube of 8x8x8 for 512 cell generation
        for _ in range(evolutions):
            #loop through the entire automaton
            next_automaton = np.zeros(np.shape(automaton)) #keep the evolved cell values here
            for x in range(8):
                for y in range(8):
                    for z in range(8):
                        #for each cell:
                        cell = 0 
                        for i in range(4):
                            #select an update mechanism at random
                            update_mechanism = np.random.choice(range(1,4))
                            rule = rules[i]
                            if(update_mechanism==1):
                                cell = model_one(x,y,z,rule,automaton)
                            elif(update_mechanism==2):
                                cell = model_two(x,y,z,rule,automaton)
                            else:
                                cell = model_three(x,y,z,rule,automaton)
                        next_automaton[x,y,z] = cell
            automaton = next_automaton.astype(int) #update the automaton ready for next iteration
        #after all the evolutions the bits in this automaton can be used as the final random sequence
        sequence =  list(automaton.flatten())
        bit_sequence.append(sequence) #flatten the automaton into a 512 bistream
    return bit_sequence

def flip_odd_bits(bit_sequence):
    for sequence in bit_sequence:
        for i in range(0,len(sequence)-1,2):
            if(sequence[i] == 0):
                sequence[i] = 1
            else:
                sequence[i] = 0
    return bit_sequence

def save_sequence(bit_sequence):
    # file_byte_array = bytearray(bit_sequence)
    with open("bin_file.txt",'w') as new_file:
        sequence = ''
        for i in range(len(bit_sequence)):
            sequence += str(bit_sequence[i])
        new_file.write(sequence)
    print('File created successfully')

start = time.time()

evolutions = 1 #the last evolution result is conv erted into the final sequence
sequences = 10 #each sequence is 512 bits
#generate a sequence of bits
bit_sequence = generate(sequences,evolutions)
# bit_sequence = flip_odd_bits(bit_sequence)
#flatten the bit sequence into a single list
flatten = itertools.chain.from_iterable
bit_sequence = flatten(bit_sequence)
#cast to binary list
bit_sequence = list(bit_sequence)
print('Zeros: {}'.format(bit_sequence.count(0)))
print('Ones: {}'.format(bit_sequence.count(1)))
# print(bit_sequence)
# bit_sequence = [bin(int(i)) for i in bit_sequence]
# print(bit_sequence)
save_sequence(bit_sequence)#save to folder

stop = time.time()
print('Compute time: {} seconds'.format(stop-start))