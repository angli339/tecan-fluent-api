import itertools
import xml.etree.ElementTree as ET

def make_element(tag: str, text: str=''):
    el = ET.Element(tag)
    el.text = text
    return el

class Object_String(ET.Element):
    def __init__(self, value: str):
        self.tag = 'Object'
        self.attrib['Type'] = 'System.String'
        self.append(make_element('string', value))

class Object_Int32(ET.Element):
    def __init__(self, value: int):
        self.tag = 'Object'
        self.attrib['Type'] = 'System.Int32'
        self.append(make_element('int', str(value)))

class ScriptGroup(ET.Element):
    def __init__(self, objects: list[ET.Element]):
        self.tag = 'ScriptGroup'
        el_objects = ET.SubElement(self, 'Objects')
        el_objects.extend(objects)

class Data_ScriptCommandDataV1(ET.Element):
    def __new__(self, device, labware_name: str=''):
        el = ET.fromstring('''
<Data Type="Tecan.Core.Instrument.Helpers.Scripting.ScriptCommandCommonDataV1">
    <ScriptCommandCommonDataV1>
    <LabwareName></LabwareName>
    <Data Type="Tecan.Core.Instrument.Helpers.Scripting.DeviceAliasStatementBaseDataV1">
        <DeviceAliasStatementBaseDataV1>
        <Alias Type="Tecan.Core.Instrument.DeviceAlias.DeviceAlias">
            <DeviceAlias>Instrument=1/Device=LIHA:1</DeviceAlias>
        </Alias>
        <ID>
            <AvailableID>USB:TECAN,MYRIUS,123456789/LIHA:1</AvailableID>
        </ID>
        </DeviceAliasStatementBaseDataV1>
    </Data>
    </ScriptCommandCommonDataV1>
</Data>''')
        el_labware_name = el.find('.//LabwareName')
        el_labware_name.text = labware_name

        el_device_alias = el.find('.//DeviceAlias')
        el_device_alias.text = "Instrument=1/Device=%s:1" % device

        el_available_id = el.find('.//AvailableID')
        el_available_id.text = "USB:TECAN,MYRIUS,123456789/%s:1" % device

        return el