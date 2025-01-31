from autotools.autobuilder import Autobuilder, log, sub, os

if __name__ == "__main__":
    sub.run("cls" if os.name == "nt" else "clear", shell=True)
    log.info("\nЗапущен автосборщик, выберите генератор:\n\tVS - Visual Studio 17 2022\n\tMinGW - MinGW Makefiles\n")
    choice: str = str(input("Ввод: "))

    match(choice):
        case "VS":
            builder: Autobuilder = Autobuilder("VS")
            builder.build()
        case "MinGW":
            builder: Autobuilder = Autobuilder("MinGW")
            builder.build()
        case _:
            log.info("Отмена....")
