import argparse

def main():



    parser = argparse.ArgumentParser()

    parser.add_argument('--sciezka_json' , type=str, help='Nalezy tu wpisac super sciezka do pliku JSON')
    parser.add_argument('--x' , type=int , help='Wpisz tu liczbe x')
    parser.add_argument('--y' , type=int , help='Wpisz tu liczbe y')
    ## stworz zmienna z ktora wpiszemy do funkcji dodaj liczby
    parser.add_argument('--z', type=int,help="Wpisz tu liczbe z")

    args = parser.parse_args()

    def dodaj_liczby(x, y , z):
        print(x+y+z)

    dodaj_liczby(args.x, args.y , args.z)


if __name__ == '__main__':
    main()