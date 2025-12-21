import xml.etree.ElementTree as ET

from .command_elements_common import *

class Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5(ET.Element):
    def __init__(self, labware: str,
                 adapterplate: str = 'EVA',
                 well_offset: int = 0,
                 well_pos_first_tip: tuple[int, int] = (0, 0),
                 compartment: int = 1,
                 first_tip_pos_xy: tuple[int, int] = (1, 1),
                 last_tip_pos_xy: tuple[int, int] = (12, 8)):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca._384.Scripting.Data.Mca384ScriptCommandUsingWellSelectionBaseDataV5'
        
        el_pos_first_tip = ET.Element('PositionFirstTip')
        el_pos_first_tip_point = ET.SubElement(el_pos_first_tip, 'Point')
        el_pos_first_tip_point_x = ET.SubElement(el_pos_first_tip_point, 'X')
        el_pos_first_tip_point_y = ET.SubElement(el_pos_first_tip_point, 'Y')
        el_pos_first_tip_point_x.text = str(well_pos_first_tip[0])
        el_pos_first_tip_point_y.text = str(well_pos_first_tip[1])

        if adapterplate != "EVA":
            raise NotImplementedError("only EVA adapterplate is implemented in Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5")

        el_adapter_plate = ET.fromstring('''
<AdapterPlate>
    <AdapterData>
        <Name>EVA (Extended Volume)</Name>
        <Type>DiTiAdapter</Type>
        <CanMountTecanDiTis>true</CanMountTecanDiTis>
        <XCount>12</XCount>
        <YCount>8</YCount>
        <XSpacing>9</XSpacing>
        <YSpacing>9</YSpacing>
        <ID>TOOLTYPE:Mca384.Adapter/TOOLNAME:DiTi96.ExtVol</ID>
        <UsableTips>
          <UsableTips>All</UsableTips>
        </UsableTips>
        <SortNumber>50</SortNumber>
        <MountColumnRowWise>false</MountColumnRowWise>
    </AdapterData>
</AdapterPlate>''')

        el_used_tip = ET.fromstring('<UsedTip><UsableTips>All</UsableTips></UsedTip>')

        el_data = ET.SubElement(self, 'Mca384ScriptCommandUsingWellSelectionBaseDataV5')
        el_data.extend([
            Data_ScriptCommandDataV1('MCA384', labware),
            make_element('WellOffset', str(well_offset)),
            el_pos_first_tip,
            make_element('Compartment', str(compartment)),
            el_adapter_plate,
            el_used_tip,
            make_element('FirstTipXPosition', str(first_tip_pos_xy[0])),
            make_element('FirstTipYPosition', str(first_tip_pos_xy[1])),
            make_element('LastTipXPosition', str(last_tip_pos_xy[0])),
            make_element('LastTipYPosition', str(last_tip_pos_xy[1])),

            make_element('Column', '0'),
            make_element('Row', '0'),
            make_element('RowOffset', '0'),
            make_element('ColumnOffset', '0'),

            make_element('OrientationPhi', '0'),
            make_element('OrientationPsi', '0'),
            make_element('OrientationTheta', '0'),

            make_element('SelectedRowsOrColumns', ''),
            make_element('SubsequentPipettingDirectionIsRow', 'False'),
        ])

class Data_Mca384PartialTipCommandBaseDataV1(ET.Element):
    def __init__(self,
                 labware: str,
                 head_position: str = 'Left',
                 adapterplate: str = 'EVA',
                 first_tip_pos_xy: tuple[int, int] = (1, 1),
                 last_tip_pos_xy: tuple[int, int] = (12, 8)):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca.Mca384.Scripting.Mca384PartialTipCommandBaseDataV1'
        
        el_head_pos = ET.Element('HeadPosition')
        el_head_pos_head_pos = ET.SubElement(el_head_pos, 'HeadPositions')
        el_head_pos_head_pos.text = head_position

        el_data = ET.SubElement(self, 'Mca384PartialTipCommandBaseDataV1')
        el_data.extend([
            make_element('PartialColumns', '12'),
            make_element('PartialRows', '8'),
            make_element('PartialColumnOffset', '0'),
            make_element('PartialRowsOffset', '0'),
            el_head_pos,
            make_element('RemoveRack', 'False'),
            make_element('WasteForDitis', ''),
            Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5(
                labware=labware,
                adapterplate=adapterplate,
                first_tip_pos_xy=first_tip_pos_xy,
                last_tip_pos_xy=last_tip_pos_xy,
            ),
        ])

class Data_Mca384PartialTipCommandBaseDataV2(ET.Element):
    def __init__(self,
                 labware: str,
                 head_position: str = 'Left',
                 adapterplate: str = 'EVA',
                 first_tip_pos_xy: tuple[int, int] = (1, 1),
                 last_tip_pos_xy: tuple[int, int] = (12, 8)):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca.Mca384.Scripting.Mca384PartialTipCommandBaseDataV2'
        
        el_head_pos = ET.Element('HeadPosition')
        el_head_pos_head_pos = ET.SubElement(el_head_pos, 'HeadPositions')
        el_head_pos_head_pos.text = head_position

        el_data = ET.SubElement(self, 'Mca384PartialTipCommandBaseDataV2')
        el_data.extend([
            make_element('PartialColumns', '12'),
            make_element('PartialRows', '8'),
            make_element('PartialColumnOffset', '0'),
            make_element('PartialRowsOffset', '0'),
            el_head_pos,
            make_element('RemoveRack', 'False'),
            make_element('WasteForDitis', ''),
            Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5(
                labware=labware,
                adapterplate=adapterplate,
                first_tip_pos_xy=first_tip_pos_xy,
                last_tip_pos_xy=last_tip_pos_xy,
            ),
        ])

class Data_Mca384PipettingWithVolumesScriptCommandDataV2(ET.Element):
    def __init__(self, volume: float, labware: str, liquid_class: str,
                 offset_xy: tuple[int, int] = (0, 0)):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca.Mca384.Scripting.Mca384PipettingWithVolumesScriptCommandDataV2'
        
        el_data = ET.SubElement(self, 'Mca384PipettingWithVolumesScriptCommandDataV2')
        el_data.extend([
            make_element('LiquidClassName', liquid_class),
            make_element('Volume', str(volume)),
            make_element('IsLiquidClassNameByExpressionEnabled', 'False'),
            make_element('LiquidClassNameBySelection', liquid_class),
            make_element('LiquidClassNameByExpression', ''),
            make_element('OffsetX', str(offset_xy[0])),
            make_element('OffsetY', str(offset_xy[1])),
            Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5(labware),
        ])

class Object_Mca384GetHeadAdapterScriptCommandDataV1(ET.Element):
    def __init__(self, head_adapter: str, air_gap_volume: int):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca._384.Scripting.Mca384GetHeadAdapterScriptCommandDataV1'
        
        el_data = ET.SubElement(self, 'Mca384GetHeadAdapterScriptCommandDataV1')
        el_data.extend([
            make_element('BlowoutAirgap', str(air_gap_volume)),
            Data_ScriptCommandDataV1('MCA384', head_adapter),
        ])

class Object_Mca384GetTipsScriptCommandDataV1(ET.Element):
    def __init__(self, labware: str,
                 air_gap_volume: int = 0,
                 adapterplate: str = 'EVA',
                 first_tip_pos_xy: tuple[int, int] = (1, 1),
                 last_tip_pos_xy: tuple[int, int] = (12, 8)):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca.Mca384.Scripting.Mca384GetTipsScriptCommandDataV1'
        
        el_data = ET.SubElement(self, 'Mca384GetTipsScriptCommandDataV1')
        el_data.extend([
            make_element('BlowoutAirgap', str(air_gap_volume)),
            Data_Mca384PartialTipCommandBaseDataV2(
                labware=labware,
                head_position = 'Center',
                adapterplate=adapterplate,
                first_tip_pos_xy=first_tip_pos_xy,
                last_tip_pos_xy=last_tip_pos_xy,
            ),
        ])

class Object_Mca384MoveArmScriptCommandDataV1(ET.Element):
    def __init__(self, type: str, speed: int, distance: float, z_offset: float, z_custom_vector: str,
                 labware: str):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Scripting.Commands.Mca384.Mca384MoveArmScriptCommandDataV1'
        
        el_data = ET.SubElement(self, 'Mca384MoveArmScriptCommandDataV1')
        el_data.extend([
            make_element('MovementType', type),
            make_element('MovementSpeed', str(speed)),
            make_element('MovementDistance', str(distance)),
            make_element('ZOffset', str(z_offset)),
            make_element('ZCustomVector', z_custom_vector),
            Data_Mca384ScriptCommandUsingWellSelectionBaseDataV5(labware),
        ])

class Object_Mca384AspirateScriptCommandDataV2(ET.Element):
    def __init__(self, volume: float, labware: str, liquid_class: str):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Scripting.Commands.Mca384.Mca384AspirateScriptCommandDataV2'
        
        el_data = ET.SubElement(self, 'Mca384AspirateScriptCommandDataV2')
        el_data.append(Data_Mca384PipettingWithVolumesScriptCommandDataV2(
            volume=volume,
            labware=labware,
            liquid_class=liquid_class,
        ))

class Object_Mca384DispenseScriptCommandDataV2(ET.Element):
    def __init__(self, volume: float, labware: str, liquid_class: str):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Scripting.Commands.Mca384.Mca384DispenseScriptCommandDataV2'
        
        el_data = ET.SubElement(self, 'Mca384DispenseScriptCommandDataV2')
        el_data.append(Data_Mca384PipettingWithVolumesScriptCommandDataV2(
            volume=volume,
            labware=labware,
            liquid_class=liquid_class,
        ))

class Object_Mca384DropTipsScriptCommandDataV1(ET.Element):
    def __init__(self, labware: str, back_position: str = 'BackToPosition'):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Mca.Mca384.Scripting.Mca384DropTipsScriptCommandDataV1'
        
        el_use_source_as_back_pos = ET.Element('UseSourceAsBackPosition')
        el_use_source_as_back_pos_backs = ET.SubElement(el_use_source_as_back_pos, 'Backs')
        el_use_source_as_back_pos_backs.text = back_position

        el_data = ET.SubElement(self, 'Mca384DropTipsScriptCommandDataV1')
        el_data.extend([
            el_use_source_as_back_pos,
            Data_Mca384PartialTipCommandBaseDataV1(
                labware=labware,
                head_position='Center',
            ),
        ])
