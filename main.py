import subprocess

from subprocess import PIPE, Popen

inputcheck="seed-phrase"

inputcheck_list=inputcheck.split(' ')


output=''

list_of_inputs=['list of 2048 words']


counter=0

#while len(output)==0:

for word in list_of_inputs:
    for i in range(0,23):
        counter=counter+1
        print(counter)
        inputcheck_list=inputcheck.split(' ')

        x_inputcheck_list=inputcheck_list
        x_inputcheck_list.insert(i, word)
        thing=' '.join((x_inputcheck_list))
        print(thing)
        #print(thing)



        command = "solana-keygen pubkey prompt://"
        with Popen(command, stdin=PIPE, stdout=PIPE, shell=True,encoding='utf-8') as process:
            output = process.communicate(input=thing)[0]
            print('')

            #print(output)
            print(len(output))
            if len(output)>0:
                print('----------ignore above------------------')
                print('')

                print('below you will find the public key and the seed phrase corresponding to this key')
                print("public key: "+str(output))
                #print("seed-phrase: "+str(inputcheck))
                print("seed-phrase: "+str(thing))

                with open("list_of_keys_3.txt", "a") as a_file:
                  a_file.write("\n")
                  a_file.write(str(output))


                #break
