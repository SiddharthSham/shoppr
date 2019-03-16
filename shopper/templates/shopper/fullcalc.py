def main():
    print("Enter your first number: ")
    x = int(input())
    print("Enter your second number: ")
    y = int(input())
    print("Choose your operation: * or /")
    z = input()
    if(z=='*'):
        print(x/y)
        main()
    elif(z=='/'):
        print(x*y)
        main()
    else:
        print("Illegal operation. Try again")
        main() 

main()