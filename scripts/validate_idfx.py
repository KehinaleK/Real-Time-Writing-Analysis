from lxml import etree

def preprocess_xml_content(content):
    # Replace &#x8; and &#x1B; with valid placeholders or remove them
    content = content.replace("&#x8;", "BACKSPACE_PLACEHOLDER")
    content = content.replace("&#x1B;", "ESCAPE_PLACEHOLDER")
    return content

def parse_xml(xml_file):
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Preprocess the content to handle &#x8; and &#x1B;
        content = preprocess_xml_content(content)
        
        root = etree.fromstring(content)
        tree = etree.ElementTree(root)
        print("XML file is well-formed.")
        return tree
    except etree.XMLSyntaxError as e:
        print(f"XML file is not well-formed: {e}")
        # Extract the error details
        error_line = e.lineno
        error_column = e.position[1]
        
        # Read the file and print the problematic character
        with open(xml_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if error_line <= len(lines):
                error_line_content = lines[error_line - 1]
                if error_column <= len(error_line_content):
                    invalid_char = error_line_content[error_column - 1]
                    print(f"Invalid character '{invalid_char}' (code {ord(invalid_char)}) at line {error_line}, column {error_column}")
                else:
                    print(f"Error column {error_column} exceeds line length at line {error_line}")
            else:
                print(f"Error line {error_line} exceeds total number of lines")

        # Attempt to locate and print the whole element and its event ID
        try:
            with open(xml_file, 'r', encoding='utf-8') as file:
                content = file.read()
                content = preprocess_xml_content(content)  # Ensure preprocessing is applied
                parser = etree.XMLParser(recover=True)
                root = etree.fromstring(content, parser=parser)
                for elem in root.iter():
                    if elem.sourceline == error_line:
                        print("Problematic element:")
                        print(etree.tostring(elem, pretty_print=True).decode())
                        # Find the parent event element and print its ID
                        event = elem.getparent()
                        while event is not None and event.tag != "event":
                            event = event.getparent()
                        if event is not None:
                            event_id = event.get("id", "unknown")
                            print(f"Problematic event ID: {event_id}")
                        break
        except Exception as ex:
            print(f"An error occurred while trying to extract the element: {ex}")
        
        return None

def validate_idfx(tree):
    root = tree.getroot()
    

    # Iterate over each event element

    # Example rule: Check for specific attributes
    for event in root.findall(".//event"):
        if "type" not in event.attrib:
            print(f"Missing 'type' attribute in event with ID {event.get('id', 'unknown')}")
        if "id" not in event.attrib:
            print(f"Missing 'id' attribute in event: {etree.tostring(event)}")
    
    # Example rule: Check if event type is 'keyboard' then check for specific child elements
    for event in root.findall(".//event[@type='keyboard']"):
        part = event.find("part")
        print(f"'part' element in keyboard event with ID {event.get('id', 'unknown')}")
        if part is not None:
            startTime = part.find("startTime")
            endTime = part.find("endTime")
            # if startTime is None:
            #     print(f"Missing 'startTime' element in event with ID {event.get('id', 'unknown')}")
            # if endTime is None:
            #     print(f"Missing 'endTime' element in event with ID {event.get('id', 'unknown')}")
        else:
            print(f"Missing 'part' element in keyboard event with ID {event.get('id', 'unknown')}")

def main():
    xml_file = '../data/idfx/test/P+S1.idfx'
    tree = parse_xml(xml_file)
    if tree is not None:
        validate_idfx(tree)

if __name__ == "__main__":
    main()
