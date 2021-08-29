import subprocess
from subprocess import PIPE, Popen
from tqdm.auto import trange
import sys
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("a", type=str, help="the address of the wallet")
    parser.add_argument("s", type=str, help="the partial seedphrase in quotes")
    parser.add_argument('-w', action="store_true", default=False, help="try single word swaps (20x slower)")
    args = parser.parse_args()

    address = args.a
    seed_partial = args.s
    try_swaps = args.w

      # Example values:
      # The real seed is: session little medal decrease humor city twist wink strong short twelve bench hurry inject hurt edit convince today price action country disease spice trend
      # seed_partial    = "session little medal humor city twist wink strong short twelve bench hurry inject hurt edit convince today price action country disease spice trend"
      # The address that we are searching for
      # address =  "7zaM9ebxa76zE5WWaAT81RSWsFBgMZeZooMJYPoXRqVn"


    seed_partial_list=seed_partial.split(sep=None)

    file = open("./bipwords.txt", "r")
    bip_words = file.read().splitlines()

    dictionary=bip_words

    done=False

    for i in trange(0,24, desc="place?"):

        for d in trange(0, len(dictionary), desc="word?", leave=False):

            word = dictionary[d]

            seed_ansatz_list=seed_partial_list.copy()
            seed_ansatz_list.insert(i, word)

            for j in trange(0, 24, desc="swap?", leave=False ):

                swappable_ansatz_list = seed_ansatz_list.copy()

                if try_swaps:
                    if j==i:
                        # don't do anything at the ith word as this was inserted, no need to swap it
                        pass
                    else:
                        # swap the jth and j+1 st words
                        temp = swappable_ansatz_list.pop(j)
                        swappable_ansatz_list.insert(j+1, temp)

                seed_ansatz_str= ' '.join((swappable_ansatz_list))

                command = "solana-keygen recover 'prompt:?key=0/0' --force"

                with Popen(command, stdin=PIPE, stdout=PIPE, stderr=subprocess.DEVNULL, shell=True,encoding='utf-8') as process:
                    output = process.communicate(input=seed_ansatz_str)[0]

                    if len(output)>0 :

                        if address in str(output):
                            done = True

                            print("\n\n\n *********************SUCCESS*********************\n\n\n")
                            print("seed-phrase: " + str(seed_ansatz_str))
                            print("address: " + str(output))

                            with open("../output/solved_seedphrase.txt", "a") as a_file:
                                a_file.write("\n")
                                a_file.write(str(seed_ansatz_str))
                                a_file.write(str(output))

                if done: break
                if not try_swaps: break
            if done: break
        if done: break

    if not done: print("Fail: seedphrase not recovered :( ")



if __name__ == "__main__":
   main()
