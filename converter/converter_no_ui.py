import sys
import json
import xml.etree.ElementTree as ET
from yaml import safe_load, safe_dump, YAMLError
import argparse
from pathlib import Path
# zaimportuje biblioetke do parsowania argumentow

## utworz zmienna parser ktora jest obiektem (zobacz w pliku parsowanie_arg.py)

import parsowanie_arg


# Reading functions
def read_json(file_path):
    file_path = Path(file_path)

    try:
        with open(file_path, "r") as file:
            data =  json.load(file)
            print(file_path , data)

            if not isinstance(data, (dict,list)):
                raise ValueError('Plik JSON nie jest dobrze sformatowany')

            return data
    except ValueError as val_err:
        print(val_err,"Brak wartosci pliku")
        return None
    except json.JSONDecodeError as e:
        print(f'Błąd przy wczytaniu pliku JSON {e}')
        return None
    except FileNotFoundError:
        print('Plik nie istnieje')
        return None



def read_yaml(file_path):
    try:
        with open(file_path, "r") as file:
           return safe_load(file)
    except ValueError as val_err:
        print(val_err)
        return None
    #YAMLError
    except YAMLError as yaml_error:
        print(yaml_error,"bład przy wczytaniu pliku")
        return None
    except FileNotFoundError:
        print("Takowy plik nie istnieje")
        return None



def read_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ValueError as val_error:
        print(val_error,"zla wartosc pliku")
        return  None
    except ET.ParseError as xml_error:
        print(xml_error,"błąd przetwarzania pliku")
        return None
    except FileNotFoundError:
        print("Plik nie istnieje")
        return None




# Writing functions
def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def write_yaml(data, file_path):
    with open(file_path, "w") as file:
        safe_dump(data, file)


def write_xml(data, file_path):
    tree = ET.ElementTree(data)
    tree.write(file_path)


# Conversion functions
def convert_json_to_yaml(json_data):
    return safe_dump(json_data)


def convert_yaml_to_json(yaml_data):
    return json.dumps(yaml_data, indent=4)


def convert_xml_to_json(xml_root):
    result = {}
    for child in xml_root:
        result[child.tag] = child.text
    return result


def convert_json_to_xml(json_data):
    root = ET.Element('root')
    for key, value in json_data.items():
        sub_elem = ET.SubElement(root, key)
        sub_elem.text = str(value)
    return root


class FileConverterApp():
    def __init__(self):
        super().__init__()




    def load_and_convert_json(self,args):

        json_path = args.json_path



        if json_path:

            json_data  = read_json(json_path)

            if json_data is None:
                return
            file_name = Path(json_path).stem

            yaml_path = Path(f'./converted_files/{file_name}.yaml')
            write_yaml(convert_json_to_yaml(json_data), yaml_path)

            xml_path =Path(f'./converted_files/{file_name}.xml')
            write_xml(convert_json_to_xml(json_data), xml_path)

    def load_and_convert_yaml(self,args):
        yaml_path= args.yaml_path
        if yaml_path:
            if yaml_path is None:
                return
            file_name = Path(yaml_path).stem
            yaml_data = read_yaml(yaml_path)
            json_path=Path(f'./converted_files/{file_name}.yaml')

            write_json(json.loads(convert_yaml_to_json(yaml_data)),json_path )




    def load_and_convert_xml(self,args):
        xml_path= args.xml_path
        if xml_path:
            if xml_path  is None:
                return
            file_name=Path(xml_path).stem
            xml_root = read_xml(xml_path)
            json_path =Path(f'./converted_files/{file_name}.json')

            write_json(convert_xml_to_json(xml_root), json_path)
#python .\converter_no_ui.py --xml_path='./ksemel.xml'

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, help="Nalezy tu wpisac sciezke do pliku json" , default='')
    parser.add_argument('--yaml_path', type=str, help="Nalezy tu wpisac sciezke do pliku yaml",default='')
    parser.add_argument('--xml_path', type=str, help="Nalezy tu wpisac sciezke do pliku xml",default='')

    args = parser.parse_args()


    ## dodaj argumenty typu  --json_path , --yaml_path, --xml_path

    app = FileConverterApp()

    ## zrob warunek ze jesli istnieje args.json_path to uruchom app.load_and_convert_json()

    if args.json_path:
        app.load_and_convert_json(args)
    if args.yaml_path:
        app.load_and_convert_yaml(args)

    if args.xml_path:
        app.load_and_convert_xml(args)


