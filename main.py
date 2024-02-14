from NFA import NFA_object
import RE2NFA

def end(code: int = 0)->None: exit(code)

def main():

    while True:
        print("Welcome to RE to NFA converter, input your RE and we drawout NFA. (type \"exit\" or \"e\" to exit)")
        re = input("Input: ")
        if (re == "exit" or re == "e"): 
            print("Program closed, goodbye!")
            end()
        try:
            converter = RE2NFA.getConverter(re)
            result = converter.process()
            result.reportOut()
        except Exception as e:
            print(e)
            end(1)

main()
end()