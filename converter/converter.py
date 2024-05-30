import sys
import json
import xml.etree.ElementTree as ET
from yaml import safe_load, safe_dump, YAMLError
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit




# Reading functions
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            data =  json.load(file)

            if not isinstance(data, (dict,list)):
                raise ValueError('Plik JSON nie jest dobrze sformatowany')
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


class FileConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Format Converter")
        layout = QVBoxLayout()

        btn_load_json = QPushButton("Load and Convert JSON", self)
        btn_load_json.clicked.connect(self.load_and_convert_json)
        layout.addWidget(btn_load_json)

        btn_load_yaml = QPushButton("Load and Convert YAML", self)
        btn_load_yaml.clicked.connect(self.load_and_convert_yaml)
        layout.addWidget(btn_load_yaml)

        btn_load_xml = QPushButton("Load and Convert XML", self)
        btn_load_xml.clicked.connect(self.load_and_convert_xml)
        layout.addWidget(btn_load_xml)

        self.setLayout(layout)

    def load_and_convert_json(self):
        json_path, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON files (*.json)")
        if json_path:
            json_data  = read_json(json_path)
            if json_data is None:
                return
            yaml_path, _ = QFileDialog.getSaveFileName(self, "Save as YAML", "", "YAML files (*.yaml)")
            if yaml_path:
                write_yaml(convert_json_to_yaml(json_data), yaml_path)
            xml_path, _ = QFileDialog.getSaveFileName(self, "Save as XML", "", "XML files (*.xml)")
            if xml_path:
                write_xml(convert_json_to_xml(json_data), xml_path)

    def load_and_convert_yaml(self):
        yaml_path, _ = QFileDialog.getOpenFileName(self, "Open YAML", "", "YAML files (*.yaml)")
        if yaml_path:
            if yaml_path is None:
                return
            yaml_data = read_yaml(yaml_path)
            json_path, _ = QFileDialog.getSaveFileName(self, "Save as JSON", "", "JSON files (*.json)")
            if json_path:
                write_json(json.loads(convert_yaml_to_json(yaml_data)), json_path)

    def load_and_convert_xml(self):
        xml_path, _ = QFileDialog.getOpenFileName(self, "Open XML", "", "XML files (*.xml)")
        if xml_path:
            if xml_path  is None:
                return
            xml_root = read_xml(xml_path)
            json_path, _ = QFileDialog.getSaveFileName(self, "Save as JSON", "", "JSON files (*.json)")
            if json_path:
                write_json(convert_xml_to_json(xml_root), json_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FileConverterApp()
    ex.show()
    sys.exit(app.exec_())
