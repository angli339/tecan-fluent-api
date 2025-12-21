import itertools
import xml.etree.ElementTree as ET

from .command_elements_common import *

class Data_LihaScriptCommandDataV1(ET.Element):
    def __init__(self, labware: str=''):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaScriptCommandDataV1'
        
        el_data = ET.SubElement(self, 'LihaScriptCommandDataV1')
        el_data.append(Data_ScriptCommandDataV1('LIHA', labware))

class Data_LiHaScriptCommandUsingTipSelectionBaseDataV1(ET.Element):
    def __init__(self, i_selected_tips: list[int], labware: str='', tip_spacing: int=9):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LiHaScriptCommandUsingTipSelectionBaseDataV1'
        
        el_elect_tips = ET.Element('SelectedTipsIndexes')
        el_elect_tips.extend([Object_Int32(i_tip) for i_tip in i_selected_tips])
        
        el_data = ET.SubElement(self, 'LiHaScriptCommandUsingTipSelectionBaseDataV1')
        el_data.extend([
            make_element('SerializedTipsIndexes'),
            el_elect_tips,
            Data_LihaScriptCommandDataV1(labware),
            make_element('TipMask'),
            make_element('TipOffset', '0'),
            make_element('TipSpacing', str(tip_spacing)),
        ])

def find_consecutive_groups(i_list: list[int]):
    for _, group in itertools.groupby(enumerate(i_list), lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

class Data_LihaScriptCommandUsingWellSelectionBaseDataV1(ET.Element):
    def __init__(self, i_selected_tips: list[int], i_selected_wells: list[int], labware: str):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaScriptCommandUsingWellSelectionBaseDataV1'

        # TODO: Find out plate type
        wellnames = ['%s%d' % (row, col) for col in range(1, 12+1) for row in 'ABCDEFGH']

        # serialize well indexes and names
        well_index_ranges = find_consecutive_groups(i_selected_wells)
        serialized_well_indexes = ""
        selected_well_names = []
        for i_start, i_end in well_index_ranges:
            if i_end == i_start:
                serialized_well_indexes += "%d;" % i_start
                selected_well_names.append(wellnames[i_start])
            elif i_end == i_start + 1:
                serialized_well_indexes += "%d;%d;" % (i_start, i_end)
                selected_well_names.append(wellnames[i_start])
                selected_well_names.append(wellnames[i_end])
            else :
                serialized_well_indexes += "%d>1>%d;" % (i_start, i_end)
                selected_well_names.append("%s - %s" % (wellnames[i_start], wellnames[i_end]))
        selected_wells_string = ', '.join(selected_well_names)

        el_data = ET.SubElement(self, 'LihaScriptCommandUsingWellSelectionBaseDataV1')
        el_data.extend([
            make_element('SerializedWellIndexes', serialized_well_indexes),
            make_element('SelectedWellsString', selected_wells_string),
            make_element('WellOffset', '0'),
            Data_LiHaScriptCommandUsingTipSelectionBaseDataV1(i_selected_tips, labware),
        ])

def liquidClassSelection_SingleByName(liquid_class: str) -> ET.Element:
        el_liquid_class_selection_mode = ET.Element('LiquidClassSelectionMode')
        el_liquid_class_selection_mode.append(make_element('LiquidClassSelectionMode', 'SingleByName'))

        el_liquid_class_names = ET.Element('LiquidClassNames')
        el_liquid_class_names.extend([Object_String('') for i in range(8)])

        return [el_liquid_class_selection_mode,
            make_element('LiquidClassNameBySelection', liquid_class),
            make_element('LiquidClassNameByExpression'),
            el_liquid_class_names]
        
class Data_LihaPipettingWithVolumesScriptCommandDataV6(ET.Element):
    def __init__(self, volumes: list[int], i_selected_tips: list[int], i_selected_wells: list[int], labware: str, liquid_class: str):
        self.tag = 'Data'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Scripting.Data.LihaPipettingWithVolumesScriptCommandDataV6'

        if len(volumes) != 8:
            raise ValueError('volumes needs to be a list of 8 numbers')
        
        el_volumes = ET.Element('Volumes')
        el_volumes.extend([Object_String(str(volume)) for volume in volumes])

        el_data = ET.SubElement(self, 'LihaPipettingWithVolumesScriptCommandDataV6')
        el_data.extend([
            el_volumes,
            make_element('IsLiquidClassNameByExpressionEnabled', 'False'),
            *liquidClassSelection_SingleByName(liquid_class),
            make_element('Compartment', '1'),
            Data_LihaScriptCommandUsingWellSelectionBaseDataV1(i_selected_tips, i_selected_wells, labware),
        ])

class DitiType(ET.Element):
    def __init__(self, diti_type: str):
        self.tag = 'DitiType'
        el_available_id = ET.SubElement(self, 'AvailableID')
        el_available_id.text = 'TOOLTYPE:LiHa.TecanDiTi/TOOLNAME:' + diti_type

class Object_LihaGetTipsScriptCommandDataV3(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 diti_type: str,
                 airgap_volume: int=10, airgap_speed: int=70, use_next_position: bool=True):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaGetTipsScriptCommandDataV3'
        
        el_data = ET.SubElement(self, 'LihaGetTipsScriptCommandDataV3')
        el_data.extend([
            Data_LiHaScriptCommandUsingTipSelectionBaseDataV1(i_selected_tips),
            make_element('AirgapVolume', str(airgap_volume)),
            make_element('AirgapSpeed', str(airgap_speed)),
            DitiType(diti_type),
            make_element('UseNextPosition', str(use_next_position)),
        ])

class Object_LihaDropTipsScriptCommandDataV2(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 diti_waste: str, skip_if_nothing_mounted: bool=False):
        self.tag = 'Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.Scripting.Data.LihaDropTipsScriptCommandDataV2'
        
        el_data = ET.SubElement(self, 'LihaDropTipsScriptCommandDataV2')
        el_data.extend([
            make_element('SkipIfNothingMounted', str(skip_if_nothing_mounted)),
            Data_LiHaScriptCommandUsingTipSelectionBaseDataV1(i_selected_tips=i_selected_tips, labware=diti_waste),
        ])

class Object_LihaPickUpScriptCommandDataV1(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int],
                 airgap_volume: int=10, airgap_speed: int=70):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaPickUpScriptCommandDataV1'

        el_data = ET.SubElement(self, 'LihaPickUpScriptCommandDataV1')
        el_data.extend([
            Data_LihaScriptCommandUsingWellSelectionBaseDataV1(i_selected_tips, i_selected_wells, labware),
            make_element('AirgapVolume', str(airgap_volume)),
            make_element('AirgapSpeed', str(airgap_speed)),
        ])

class Object_LihaSetTipsBackScriptCommandDataV1(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int]):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaSetTipsBackScriptCommandDataV1'

        el_data = ET.SubElement(self, 'LihaSetTipsBackScriptCommandDataV1')
        el_data.extend([
            Data_LihaScriptCommandUsingWellSelectionBaseDataV1(i_selected_tips, i_selected_wells, labware),
        ])

class Object_LihaAspirateScriptCommandDataV5(ET.Element):
    def __init__(self, volumes: list[int], i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int], liquid_class: str,
                 is_switch_container_source_enabled: bool=False):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaAspirateScriptCommandDataV5'

        el_data = ET.SubElement(self, 'LihaAspirateScriptCommandDataV5')
        el_data.extend([
            make_element('IsSwitchContainerSourceEnabled', str(is_switch_container_source_enabled)),
            make_element('OffsetX', '0'),
            make_element('OffsetY', '0'),
            Data_LihaPipettingWithVolumesScriptCommandDataV6(
                volumes=volumes,
                i_selected_tips=i_selected_tips,
                labware=labware,
                i_selected_wells=i_selected_wells,
                liquid_class=liquid_class),
        ])

class LihaDispenseScriptCommandDataV4(ET.Element):
    def __init__(self, volumes: list[int], i_selected_tips: list[int],
                 labware: str,  i_selected_wells: list[int], liquid_class: str):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaDispenseScriptCommandDataV4'

        el_data = ET.SubElement(self, 'LihaDispenseScriptCommandDataV4')
        el_data.extend([
            make_element('OffsetX', '0'),
            make_element('OffsetY', '0'),
            Data_LihaPipettingWithVolumesScriptCommandDataV6(
                volumes=volumes,
                i_selected_tips=i_selected_tips,
                labware=labware,
                i_selected_wells=i_selected_wells,
                liquid_class=liquid_class),
        ])

class Object_LihaMixScriptCommandDataV4(ET.Element):
    def __init__(self, n_cycles: int, volumes: list[int], i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int], liquid_class: str):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaMixScriptCommandDataV4'

        el_data = ET.SubElement(self, 'LihaMixScriptCommandDataV4')
        el_data.extend([
            make_element('Cycles', str(n_cycles)),
            make_element('OffsetX', '0'),
            make_element('OffsetY', '0'),
            Data_LihaPipettingWithVolumesScriptCommandDataV6(
                volumes=volumes,
                i_selected_tips=i_selected_tips,
                labware=labware,
                i_selected_wells=i_selected_wells,
                liquid_class=liquid_class),
        ])

class Object_LihaMoveArmScriptCommandDataV2(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int], compartment: int,
                 movement_type: str, movement_speed: float,
                 z_offset: float, z_custom_vector: str, distance: int):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaMoveArmScriptCommandDataV2'

        el_data = ET.SubElement(self, 'LihaMoveArmScriptCommandDataV2')
        el_data.extend([
            Data_LihaScriptCommandUsingWellSelectionBaseDataV1(i_selected_tips, i_selected_wells, labware),
            make_element('Compartment', str(compartment)),
            make_element('MovementType', movement_type),
            make_element('MovementSpeed', "%.1f" % movement_speed),
            make_element('ZOffset', "%.1f" % z_offset),
            make_element('ZCustomVector', z_custom_vector),
            make_element('Distance', str(distance)),
        ])

class Object_LihaDetectLiquidScriptCommandDataV3(ET.Element):
    def __init__(self, i_selected_tips: list[int],
                 labware: str, i_selected_wells: list[int], compartment: int,
                 sensitivity_ex: int, detection_speed: int, offset_x: int, offset_y: int):
        self.tag='Object'
        self.attrib['Type'] = 'Tecan.Core.Instrument.Devices.LiHa.Scripting.LihaDetectLiquidScriptCommandDataV3'

        el_data = ET.SubElement(self, 'LihaDetectLiquidScriptCommandDataV3')
        el_data.extend([
            make_element('SensitivityEx', str(sensitivity_ex)),
            make_element('DetectionSpeed', str(detection_speed)),
            make_element('Compartment', str(compartment)),
            make_element('OffsetX', str(offset_x)),
            make_element('OffsetY', str(offset_y)),
            Data_LihaScriptCommandUsingWellSelectionBaseDataV1(i_selected_tips, i_selected_wells, labware),
        ])