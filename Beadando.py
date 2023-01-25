import base64
import click


@click.group
def mycommands():
    pass


@click.command()
def list_variables():
    filename = ".env"
    with open(filename, "r", encoding="utf-8") as f:
        variable_list = f.read().splitlines()
        for idx, variable in enumerate(variable_list):
            print(f"({idx}) -> {variable}")


@click.command()
def list_decoded_variables():
    mydict = {}
    filename = ".env"
    with open(filename, "r", encoding="utf-8") as f:
        for sor in f:
            try:
                [valtozo, b64_ertek] = sor.rstrip().split("=", 1)
            except ValueError:
                continue
            ertek = base64.b64decode(b64_ertek.encode("utf-8")).decode("utf-8")
            mydict[valtozo] = ertek

    idx = 0
    for key, value in mydict.items():
        print(f"({idx}) -> {key}={value}")
        idx += 1


@click.command()
@click.argument("envfile", type=click.Path(exists=False), required=0)
@click.option(
    "-n",
    "--name",
    prompt="Enter the name of variable",
    help="The name of environmental variable",
)
@click.option(
    "-v",
    "--value",
    prompt="Enter the value of the variable",
    help="The environmental variable value",
)
def add_new_variable(name: str, value: str, envfile: str):
    filename = envfile if envfile is not None else ".env"
    with open(filename, "a+", encoding="utf-8") as f:
        b64_value = base64.b64encode(value.encode("utf-8")).decode("utf-8")
        f.write(f"{name}={b64_value}\n")


@click.command()
@click.argument("idx", type=int, required=1)
def delete_variable(idx: int):
    filename = ".env"
    with open(filename, "r") as f:
        variable_list = f.read().splitlines()
        variable_list.pop(idx)
    with open(filename, "w") as f:
        f.write("\n".join(variable_list))
        f.write("\n")


@click.command()
@click.option(
    "-n",
    "--name",
    prompt="Enter the name of variable what you want to modify",
    help="The name of environmental variable to modify the value",
)
@click.option(
    "-v",
    "--new_value",
    prompt="Enter the new value of the variable",
    help="The environmental variable new value",
)
def update_variable(name: str, new_value: str):
    filename = ".env"
    mydict = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                [variablename, b64_value] = line.rstrip().split("=", 1)
            except ValueError:
                continue
            value = base64.b64decode(b64_value.encode("utf-8")).decode("utf-8")
            mydict[variablename] = value

    for k, v in mydict.items():
        if k == name:
            mydict[k] = new_value

    with open(filename, "w", encoding="utf-8") as f:
        for k, v in mydict.items():
            tob64 = base64.b64encode(v.encode("utf-8")).decode("utf-8")
            f.write(f"{k}={tob64}\n")


mycommands.add_command(list_variables)
mycommands.add_command(list_decoded_variables)
mycommands.add_command(add_new_variable)
mycommands.add_command(delete_variable)
mycommands.add_command(update_variable)


if __name__ == "__main__":
    mycommands()
